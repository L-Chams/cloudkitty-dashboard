# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
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

from django import forms
from django.forms.forms import NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _


class SelfHandlingMixin(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        if not hasattr(self, "handle"):
            raise NotImplementedError("%s does not define a handle method."
                                      % self.__class__.__name__)
        super().__init__(*args, **kwargs)


class SelfHandlingForm(SelfHandlingMixin, forms.Form):
    """A base Form class which includes processing logic in its subclasses."""
    required_css_class = 'required'

    def api_error(self, message):
        """Adds an error to the form's error dictionary.

        It can be used after validation based on problems reported via the API.
        This is useful when you wish for API errors to appear as errors on the
        form rather than using the messages framework.
        """
        self.add_error(NON_FIELD_ERRORS, message)

    def set_warning(self, message):
        """Sets a warning on the form.

        Unlike NON_FIELD_ERRORS, this doesn't fail form validation.
        """
        self.warnings = self.error_class([message])


class DateForm(forms.Form):
    """A simple form for selecting a range of time."""

    start = forms.DateField(input_formats=("%Y-%m-%d",))
    end = forms.DateField(input_formats=("%Y-%m-%d",))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start'].widget.attrs['data-date-format'] = "yyyy-mm-dd"
        self.fields['end'].widget.attrs['data-date-format'] = "yyyy-mm-dd"


class CheckBoxForm(forms.Form):
    """A form for selecting fields to group by in the rating summary."""

    checkbox_fields = ["type", "id", "user_id", "project_id"]

    for field in checkbox_fields:
        locals()[field] = forms.BooleanField(required=False)

    def get_selected_fields(self):
        """Return list of selected groupby fields."""
        if not self.is_valid():
            return []

        # Get all selected checkbox fields
        selected = [field for field in self.checkbox_fields if 
                    self.cleaned_data.get(field)]

        # Return the selected fields, empty list if none selected
        return selected
