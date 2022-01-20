import datetime
from django.conf import settings
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Document
        fields = ('url', 'name', 'doc_file', 'owner', 'shared_with', 'owner_username')

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        action = self.context.get('view').action
        if action in ['update', 'partial_update']:
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
        return super(DocumentSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        date = str(datetime.datetime.now())
        path = str(settings.BASE_DIR) + instance.doc_file.url
        action = f"\n{date} --- UPDATE by {user}\n"
        self.add_action_entry_to_file(path, action=action)
        validated_data['doc_file'] = instance.doc_file
        return super(DocumentSerializer, self).update(instance, validated_data)

    def validate(self, attrs):
        print("attrs", attrs)
        return attrs

    def add_action_entry_to_file(self, path, action=""):
        with open(path, 'a') as f:
            f.write(action)





