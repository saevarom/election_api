from rest_framework_nested.relations import NestedHyperlinkedRelatedField


class NestedHyperlinkedIdentityField(NestedHyperlinkedRelatedField):
    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, 'The `view_name` argument is required.'
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super(NestedHyperlinkedIdentityField, self).__init__(view_name=view_name, **kwargs)

    def use_pk_only_optimization(self):
        return False


import rest_framework.serializers
try:
    from rest_framework.utils.field_mapping import get_nested_relation_kwargs
except ImportError:
    pass  # passing because NestedHyperlinkedModelSerializer can't be used anyway
#    if version too old.


class NestedHyperlinkedModelSerializer(rest_framework.serializers.HyperlinkedModelSerializer):
    """
    A type of `ModelSerializer` that uses hyperlinked relationships with compound keys instead
    of primary key relationships.  Specifically:

    * A 'url' field is included instead of the 'id' field.
    * Relationships to other instances are hyperlinks, instead of primary keys.

    NOTE: this only works with DRF 3.1.0 and above.
    """
    parent_lookup_field = 'parent'
    parent_lookup_related_field = 'pk'
    parent_lookup_url_kwarg = 'parent_pk'

    serializer_url_field = NestedHyperlinkedIdentityField

    def __init__(self, *args, **kwargs):
        self.parent_lookup_field = kwargs.pop('parent_lookup_field', self.parent_lookup_field)
        self.parent_lookup_related_field = kwargs.pop('parent_lookup_related_field', self.parent_lookup_related_field)
        self.parent_lookup_url_kwarg = kwargs.pop('parent_lookup_url_kwarg', self.parent_lookup_url_kwarg)

        return super(NestedHyperlinkedModelSerializer, self).__init__(*args, **kwargs)

    def build_url_field(self, field_name, model_class):
        field_class, field_kwargs = super(NestedHyperlinkedModelSerializer, self).build_url_field(field_name, model_class)
        field_kwargs['parent_lookup_field'] = self.parent_lookup_field
        field_kwargs['parent_lookup_related_field'] = self.parent_lookup_related_field
        field_kwargs['parent_lookup_url_kwarg'] = self.parent_lookup_url_kwarg

        return field_class, field_kwargs

    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships.
        """
        class NestedSerializer(NestedHyperlinkedModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = '__all__'

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs
