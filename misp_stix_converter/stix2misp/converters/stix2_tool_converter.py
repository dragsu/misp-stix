#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ... import Mapping
from ..exceptions import UnknownParsingFunctionError
from .stix2converter import (
    ExternalSTIX2Converter, InternalSTIX2Converter, STIX2Converter,
    _MAIN_PARSER_TYPING)
from .stix2mapping import (
    ExternalSTIX2Mapping, InternalSTIX2Mapping, STIX2Mapping)
from abc import ABCMeta
from pymisp import MISPGalaxyCluster
from stix2.v20.sdo import Tool as Tool_v20
from stix2.v21.sdo import Tool as Tool_v21
from typing import Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..external_stix2_to_misp import ExternalSTIX2toMISPParser
    from ..internal_stix2_to_misp import InternalSTIX2toMISPParser

_TOOL_TYPING = Union[
    Tool_v20, Tool_v21
]


class STIX2ToolMapping(STIX2Mapping, metaclass=ABCMeta):
    __tool_meta_mapping = Mapping(
        aliases='synonyms',
        tool_types='tool_types',
        tool_version='tool_version'
    )

    @classmethod
    def tool_meta_mapping(cls) -> dict:
        return cls.__tool_meta_mapping


class STIX2ToolConverter(STIX2Converter, metaclass=ABCMeta):
    def __init__(self, main: _MAIN_PARSER_TYPING):
        self._set_main_parser(main)

    def _create_cluster(self, tool: _TOOL_TYPING,
                        description: Optional[str] = None,
                        galaxy_type: Optional[str] = None) -> MISPGalaxyCluster:
        tool_args = self._create_cluster_args(
            tool, galaxy_type, description=description
        )
        meta = self._handle_meta_fields(tool)
        if hasattr(tool, 'external_references'):
            meta.update(
                self._handle_external_references(tool.external_references)
            )
        if hasattr(tool, 'kill_chain_phases'):
            meta['kill_chain'] = self._handle_kill_chain_phases(
                tool.kill_chain_phases
            )
        if hasattr(tool, 'labels'):
            self._handle_labels(meta, tool.labels)
        if meta:
            tool_args['meta'] = meta
        return self._create_misp_galaxy_cluster(tool_args)


class ExternalSTIX2ToolMapping(
        STIX2ToolMapping, ExternalSTIX2Mapping):
    pass


class ExternalSTIX2ToolConverter(
        STIX2ToolConverter, ExternalSTIX2Converter):
    def __init__(self, main: 'ExternalSTIX2toMISPParser'):
        super().__init__(main)
        self._mapping = ExternalSTIX2ToolMapping
    
    def parse(self, tool_ref: str):
        tool = self.main_parser._get_stix_object(tool_ref)
        self._parse_galaxy(tool)


class InternalSTIX2ToolMapping(
        STIX2ToolMapping, InternalSTIX2Mapping):
    __script_object_mapping = Mapping(
        name=STIX2Mapping.filename_attribute(),
        description=InternalSTIX2Mapping.comment_text_attribute(),
        x_misp_language=STIX2Mapping.language_attribute(),
        x_misp_script=InternalSTIX2Mapping.script_attribute(),
        x_misp_state=InternalSTIX2Mapping.state_attribute()
    )

    @classmethod
    def script_object_mapping(cls) -> dict:
        return cls.__script_object_mapping


class InternalSTIX2ToolConverter(
        STIX2ToolConverter, InternalSTIX2Converter):
    def __init__(self, main: 'InternalSTIX2toMISPParser'):
        super().__init__(main)
        self._mapping = InternalSTIX2ToolMapping
    
    def parse(self, tool_ref: str):
        tool = self.main_parser._get_stix_object(tool_ref)
        feature = self._handle_mapping_from_labels(tool.labels, tool.id)
        try:
            parser = getattr(self, feature)
        except AttributeError:
            raise UnknownParsingFunctionError(feature)
        try:
            parser(tool)
        except Exception as exception:
            self.main_parser._tool_error(tool.id, exception)

    def _parse_script_object(self, tool: _TOOL_TYPING):
        misp_object = self._create_misp_object('script', tool)
        for attribute in self._generic_parser(tool, feature='script'):
            misp_object.add_attribute(**attribute)
        if hasattr(tool, 'x_misp_script_as_attachment'):
            attribute = {
                'type': 'attachment',
                'object_relation': 'script-as-attachment'
            }
            if isinstance(tool.x_misp_script_as_attachment, dict):
                attribute.update(tool.x_misp_script_as_attachment)
            else:
                attribute['value'] = tool.x_misp_script_as_attachment
            misp_object.add_attribute(**attribute)
        self.main_parser._add_misp_object(misp_object, tool)
