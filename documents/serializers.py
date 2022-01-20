import datetime
from time import sleep
from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.CharField(source="owner.id", read_only=True)
    owner = serializers.PrimaryKeyRelatedField(source="owner.username", read_only=True)

    class Meta:
        model = Document
        fields = ('url', 'name', 'doc_file', 'owner', 'shared_with', 'current_editors', 'owner_id')

    def get_extra_kwargs(self):

        extra_kwargs = super().get_extra_kwargs()
        action = self.context.get('view').action
        current_user = self.context.get('request').user
        if action in ['list']:
            instance_list = self.instance
            active_instances = [ins for ins in instance_list if current_user in ins.current_editors.all()]
            for ins in active_instances:
                ins.current_editors.remove(current_user)
        if action in ['update', 'partial_update', 'retrieve']:
            if self.instance:
                if self.instance.owner == current_user:
                    # the owner is editing right now
                    pass
                self.instance.current_editors.add(self.context.get('request').user)
            doc_file_kwargs = extra_kwargs.get('doc_file', {})
            shared_with_kwargs = extra_kwargs.get('shared_with', {})
            doc_file_kwargs['read_only'] = True
            shared_with_kwargs['read_only'] = False
            extra_kwargs['doc_file'] = doc_file_kwargs
            extra_kwargs['shared_with'] = shared_with_kwargs

        if action in ['create']:
            doc_file_kwargs = extra_kwargs.get('doc_file', {})
            shared_with_kwargs = extra_kwargs.get('shared_with', {})
            doc_file_kwargs['read_only'] = False
            shared_with_kwargs['read_only'] = True
            extra_kwargs['doc_file'] = doc_file_kwargs
            extra_kwargs['shared_with'] = shared_with_kwargs

        extra_kwargs['current_editors'] = {'read_only': True}

        return extra_kwargs

    def create(self, validated_data):
        mem_file = validated_data['doc_file']
        user = self.context.get('request').user
        date = str(datetime.datetime.now())
        action = f"\n{date} --- CREATE by {user}\n"
        mem_contents = mem_file.file.getvalue()
        contents = mem_contents  + bytes(action, 'utf-8')
        mem_file.file.write(contents)
        validated_data['doc_file'] = mem_file
        validated_data['owner'] = user
        return super(DocumentSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        date = str(datetime.datetime.now())
        path = str(settings.BASE_DIR) + instance.doc_file.url
        action = f"\n{date} --- UPDATE by {user}\n"
        self.add_action_entry_to_file(path, action=action)
        validated_data['doc_file'] = instance.doc_file
        if instance.owner != user and user in instance.current_editors.all():
            instance = Document.objects.select_for_update(skip_locked=True).get(id=instance.id)
            return super(DocumentSerializer, self).update(instance, validated_data)
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            for sw in validated_data.get('shared_with', instance.shared_with.all()):
                instance.shared_with.add(sw)
            instance.doc_file = validated_data.get('doc_file', instance.doc_file)
            instance.save()
        return instance


    def validate(self, attrs):
        return attrs

    def add_action_entry_to_file(self, path, action=""):
        with open(path, 'a') as f:
            f.write(action)





