# Copyright 2018 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from django.utils.translation import gettext_lazy as _

from horizon import tables


class SummaryTable(tables.DataTable):
    """This table formats a summary for the given tenant."""

    res_type = tables.Column('type', verbose_name=_('Metric Type'))
    res_id = tables.Column('id', verbose_name=_('ID'))
    user_id = tables.Column('user_id', verbose_name=_('User ID'))
    project_id = tables.Column('project_id', verbose_name=_('Project ID'))
    rate = tables.Column('rate', verbose_name=_('Rate'))

    def __init__(self, request, data=None, needs_form_wrapper=None, **kwargs):
        super().__init__(request, data, needs_form_wrapper, **kwargs)
        
        # Hide columns based on checkbox selection
        if request.GET.get('id') != 'true':
            self.columns['res_id'].classes = ['hidden']
        if request.GET.get('user_id') != 'true':
            self.columns['user_id'].classes = ['hidden']
        if request.GET.get('project_id') != 'true':
            self.columns['project_id'].classes = ['hidden']

    class Meta(object):
        name = "summary"
        verbose_name = _("Summary")

    def get_object_id(self, datum):
        # prevents the table from displaying the same ID for different rows
        id_parts = []
        for field in ['type', 'id', 'user_id', 'project_id']:
            if field in datum and datum[field]:
                id_parts.append(str(datum[field]))
        
        if id_parts:
            return '_'.join(id_parts)
        return 'unknown'
