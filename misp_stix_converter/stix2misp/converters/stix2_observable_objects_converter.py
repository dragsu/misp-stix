#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .stix2_observable_converter import (
    ExternalSTIX2ObservableMapping, InternalSTIX2ObservableMapping,
    STIX2ObservableConverter)
from abc import ABCMeta
from pymisp import AbstractMISP, MISPAttribute, MISPObject
from stix2.v21.observables import (
    Artifact, AutonomousSystem, Directory, DomainName, EmailMessage, File,
    NetworkTraffic, Process, Software, UserAccount, WindowsRegistryKey,
    X509Certificate)
from stix2.v21.sdo import Malware
from typing import Dict, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..external_stix2_to_misp import ExternalSTIX2toMISPParser
    from .stix2_malware_converter import (
        ExternalSTIX2MalwareConverter, InternalSTIX2MalwareConverter)

_MISP_OBJECTS_PATH = AbstractMISP().misp_objects_path

# TYPINGS
_MAIN_CONVERTER_TYPING = Union[
    'ExternalSTIX2MalwareConverter', 'InternalSTIX2MalwareConverter'
]
_MISP_CONTENT_TYPING = Union[
    MISPAttribute, MISPObject
]
_OBSERVABLE_TYPING = Union[
    Artifact, AutonomousSystem, Directory, DomainName, EmailMessage, File,
    NetworkTraffic, Process, Software, UserAccount, WindowsRegistryKey,
    X509Certificate
]


class STIX2ObservableObjectConverter(STIX2ObservableConverter):
    def __init__(self, main: 'ExternalSTIX2toMISPParser'):
        self._set_main_parser(main)
        self._mapping = ExternalSTIX2ObservableMapping

    def _create_misp_attribute(
            self, attribute_type: str, observable: DomainName,
            feature: Optional[str] = 'value',
            **kwargs: Dict[str, str]) -> MISPAttribute:
        return {
            'value': getattr(observable, feature), 'type': attribute_type,
            **kwargs, **self.main_parser._sanitise_attribute_uuid(observable.id)
        }

    def _create_misp_object_from_observable_object(
            self, name: str, observable: _OBSERVABLE_TYPING) -> MISPObject:
        misp_object = MISPObject(
            name, force_timestamps=True,
            misp_objects_path_custom=_MISP_OBJECTS_PATH
        )
        self.main_parser._sanitise_object_uuid(
            misp_object, observable.get('id')
        )
        return misp_object

    def _parse_artifact_observable_object(
            self, artifact_ref: str) -> MISPObject:
        observable = self.main_parser._observable[artifact_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_object']
        artifact = observable['observable']
        artifact_object = self._create_misp_object_from_observable_object(
            'artifact', artifact
        )
        for attribute in super()._parse_artifact_observable(artifact):
            artifact_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self._main_parser._add_misp_object(
            artifact_object, artifact
        )
        observable['misp_object'] = misp_object
        return misp_object

    def _parse_as_observable_object(self, as_ref: str) -> _MISP_CONTENT_TYPING:
        observable = self.main_parser._observable[as_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable.get(
                'misp_object', observable.get('misp_attribute')
            )
        autonomous_system = observable['observable']
        attributes = tuple(
            self._parse_ip_addresses_belonging_to_AS(autonomous_system.id)
        )
        observable['used'][self.event_uuid] = True
        if attributes:
            AS_object = self._create_misp_object_from_observable_object(
                'asn', autonomous_system
            )
            value = f'AS{autonomous_system.number}'
            AS_object.add_attribute(
                'asn', value,
                uuid=self.main_parser._create_v5_uuid(
                    f'{autonomous_system.id} - asn - {value}'
                )
            )
            for *attribute, kwargs in attributes:
                AS_object.add_attribute(*attribute, **kwargs)
            misp_object = self.main_parser._add_misp_object(
                AS_object, autonomous_system
            )
            observable['misp_object'] = misp_object
            return misp_object
        attribute = {
            'type': 'AS', 'value': f'AS{autonomous_system.number}',
            **self.main_parser._sanitise_attribute_uuid(autonomous_system.id)
        }
        misp_attribute = self.main_parser._add_misp_attribute(
            attribute, autonomous_system
        )
        observable['misp_attribute'] = misp_attribute
        return misp_attribute

    def _parse_directory_observable_object(
            self, directory_ref: str, child: Optional[str] = None
            ) -> _MISP_CONTENT_TYPING:
        observable = self.main_parser._observable[directory_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable.get('misp_object', observable['misp_attribute'])
        directory = observable['observable']
        attributes = tuple(super()._parse_directory_observable(directory))
        observable['used'][self.event_uuid] = True
        force_object = (
            len(attributes) > 1 or any(
                ref != child for ref in getattr(directory, 'contains_refs', [])
            )
        )
        if force_object:
            directory_object = self._create_misp_object_from_observable_object(
                'directory', directory
            )
            for attribute in attributes:
                directory_object.add_attribute(**attribute)
            misp_object = self.main_parser._add_misp_object(
                directory_object, directory
            )
            observable['misp_object'] = misp_object
            if hasattr(directory, 'contains_refs'):
                for ref in directory.contains_refs:
                    feature = f"_parse_{ref.split('--')[0]}_observable_object"
                    referenced_object = (
                        self.main_parser._observable[child]['observable']
                        if child == ref else getattr(self, feature)(ref)
                    )
                    misp_object.add_reference(
                        referenced_object.uuid, 'contains'
                    )
            return misp_object
        if child is None:
            attribute = attributes[0]
            misp_attribute = self.main_parser._add_misp_attribute(
                {
                    'type': attribute['type'], 'value': attribute['value'],
                    **self.main_parser._sanitise_attribute_uuid(
                        directory.id
                    )
                },
                directory
            )
            observable['misp_attribute'] = misp_attribute
            return misp_attribute
        file_object = self.main_parser._observable[child]['observable']
        file_object.add_attribute(**attributes[0])
        observable['misp_object'] = file_object
        return misp_object

    def _parse_domain_observable_object(
            self, domain_ref: str) -> _MISP_CONTENT_TYPING:
        observable = self.main_parser._observable[domain_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable.get(
                'misp_object', observable.get('misp_attribute')
            )
        domain_name = observable['observable']
        if hasattr(domain_name, 'resolves_to_refs'):
            domain_object = self._create_misp_object_from_observable_object(
                'domain-ip', domain_name
            )
            for attribute in super()._parse_domain_observable(domain_name):
                domain_object.add_attribute(**attribute)
            observable['used'][self.event_uuid] = True
            misp_object = self.main_parser._add_misp_object(
                domain_object, domain_name
            )
            observable['misp_object'] = misp_object
            for reference in domain_name.resolves_to_refs:
                if reference.split('--')[0] == 'domain-name':
                    referenced_domain = self._parse_domain_observable_object(
                        reference
                    )
                    misp_object.add_reference(
                        referenced_domain.uuid, 'resolves-to'
                    )
                    continue
                resolved_ip = self.main_parser._observable[reference]
                ip_address = resolved_ip['observable']
                *attribute, kwargs = super()._parse_ip_observable(ip_address)
                misp_object.add_attribute(*attribute, **kwargs)
                resolved_ip['used'][self.event_uuid] = True
                resolved_ip['misp_object'] = misp_object
                if hasattr(ip_address, 'resolves_to_refs'):
                    for referenced_mac in ip_address.resolves_to_refs:
                        resolved_mac = self.main_parser._observable[
                            referenced_mac
                        ]
                        mac_address = resolved_mac['observable']
                        attribute = self._create_misp_attribute(
                            'mac-address', mac_address,
                            comment=f'Resolved by {ip_address.value}'
                        )
                        resolved_mac['used'][self.event_uuid] = True
                        misp_attribute = self.main_parser._add_misp_attribute(
                            attribute, mac_address
                        )
                        resolved_mac['misp_attribute'] = misp_attribute
                        misp_object.add_reference(
                            misp_attribute.uuid, 'resolves-to'
                        )
            return misp_object
        observable['used'][self.event_uuid] = True
        misp_attribute = self.main_parser._add_misp_attribute(
            self._create_misp_attribute('domain', domain_name), domain_name
        )
        observable['misp_attribute'] = misp_attribute
        return misp_attribute

    def _parse_email_address_observable_object(
            self, email_address_ref: str) -> _MISP_CONTENT_TYPING:
        observable = self.main_parser._observable[email_address_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable.get(
                'misp_attribute', observable.get('misp_object')
            )
        email_address = observable['observable']
        if hasattr(email_address, 'belongs_to_ref'):
            user_account_object = self._parse_user_account_observable_object(
                email_address.belongs_to_ref
            )
            user_account_object.add_attribute(
                'email', email_address.value, **{
                    'uuid': self.main_parser._create_v5_uuid(
                        f'{email_address.id} - email - {email_address.value}'
                    )
                }
            )
            observable['used'][self.event_uuid] = True
            observable['misp_object'] = user_account_object
            return user_account_object
        misp_attribute = self.main_parser._add_misp_attribute(
            self._create_misp_attribute('email', email_address), email_address
        )
        observable['used'][self.event_uuid] = True
        observable['misp_attribute'] = misp_attribute
        return misp_attribute

    def _parse_email_message_observable_object(
            self, email_message_ref: str) -> MISPObject:
        observable = self.main_parser._observable[email_message_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_object']
        email_message = observable['observable']
        email_object = self._create_misp_object_from_observable_object(
            'email', email_message
        )
        for attribute in super()._parse_email_message_observable(email_message):
            email_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(
            email_object, email_message
        )
        observable['misp_object'] = misp_object
        if hasattr(email_message, 'from_ref'):
            observable = self.main_parser._observable[email_message.from_ref]
            attributes = super()._parse_email_reference_observable(
                observable['observable'], 'from'
            )
            for *attribute, kwargs in attributes:
                misp_object.add_attribute(*attribute, **kwargs)
            observable['used'][self.event_uuid] = True
            observable['misp_object'] = misp_object
        for feature in ('to', 'bcc', 'cc'):
            field = f'{feature}_refs'
            if hasattr(email_message, field):
                for reference in getattr(email_message, field):
                    observable = self.main_parser._observable[reference]
                    attributes = super()._parse_email_reference_observable(
                        observable['observable'], feature
                    )
                    for *attribute, kwargs in attributes:
                        misp_object.add_attribute(*attribute, **kwargs)
                    observable['used'][self.event_uuid] = True
                    observable['misp_object'] = misp_object
        if hasattr(email_message, 'additional_header_fields'):
            attributes = super()._parse_email_additional_header(
                email_message.additional_header_fields
            )
            for attribute in attributes:
                misp_object.add_attribute(**attribute)
        return misp_object

    def _parse_file_observable_object(self, file_ref: str) -> MISPObject:
        observable = self.main_parser._observable[file_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_object']
        _file = observable['observable']
        file_object = self._create_misp_object_from_observable_object(
            'file', _file
        )
        for attribute in super()._parse_file_observable(_file):
            file_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(file_object, _file)
        observable['misp_object'] = misp_object
        if hasattr(_file, 'content_ref'):
            artifact_object = self._parse_artifact_observable_object(
                _file.content_ref
            )
            artifact_object.add_reference(misp_object.uuid, 'content-of')
        if hasattr(_file, 'parent_directory_ref'):
            self._parse_directory_observable_object(
                _file.parent_directory_ref, child=_file.id
            )
        return misp_object

    def _parse_ip_addresses_belonging_to_AS(self, AS_id: str):
        for content in self.main_parser._observable.values():
            observable = content['observable']
            if observable.type not in ('ipv4-addr', 'ipv6-addr'):
                continue
            if AS_id in getattr(observable, 'belongs_to_refs', []):
                content['used'][self.event_uuid] = True
                yield super()._parse_ip_belonging_to_AS_observable(observable)

    def _parse_ip_address_observable_object(
            self, ip_address_ref: str) -> _MISP_CONTENT_TYPING:
        observable = self.main_parser._observable[ip_address_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable.get(
                'misp_attribute', observable.get('misp_object')
            )
        ip_address = observable['observable']
        observable['used'][self.event_uuid] = True
        misp_attribute = self.main_parser._add_misp_attribute(
            self._create_misp_attribute('ip-dst', ip_address), ip_address
        )
        observable['misp_attribute'] = misp_attribute
        return misp_attribute

    def _parse_mac_address_observable_object(
            self, mac_address_ref: str) -> MISPAttribute:
        observable = self.main_parser._observable[mac_address_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_attribute']
        mac_address = observable['observable']
        misp_attribute = self.main_parser._add_misp_attribute(
            self._create_misp_attribute('mac-address', mac_address), mac_address
        )
        observable['used'][self.event_uuid] = True
        observable['misp_attribute'] = misp_attribute
        return misp_attribute

    def _parse_mutex_observable_object(self, mutex_ref: str) -> MISPAttribute:
        observable = self.main_parser._observable[mutex_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_attribute']
        mutex = observable['observable']
        misp_attribute = self.main_parser._add_misp_attribute(
            self._create_misp_attribute('mutex', mutex), mutex
        )
        observable['used'][self.event_uuid] = True
        observable['misp_attribute'] = misp_attribute
        return misp_attribute

    def _parse_network_connection_observable_object(
            self, observable: NetworkTraffic) -> MISPObject:
        connection_object = self._create_misp_object_from_observable_object(
            'network-connection', observable
        )
        for attribute in super()._parse_network_traffic_observable(observable):
            connection_object.add_attribute(**attribute)
        protocols = super()._parse_network_connection_observable(observable)
        for *attribute, kwargs in protocols:
            connection_object.add_attribute(*attribute, **kwargs)
        return connection_object

    def _parse_network_socket_observable_object(
            self, observable: NetworkTraffic) -> MISPObject:
        socket_object = self._create_misp_object_from_observable_object(
            'network-socket', observable
        )
        for attribute in super()._parse_network_traffic_observable(observable):
            socket_object.add_attribute(**attribute)
        for attribute in super()._parse_network_socket_observable(observable):
            socket_object.add_attribute(**attribute)
        return socket_object

    def _parse_network_traffic_observable_object(
            self, network_traffic_ref: str) -> MISPObject:
        observable = self.main_parser._observable[network_traffic_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_object']
        network_traffic = observable['observable']
        feature = self._parse_network_traffic_observable_fields(network_traffic)
        network_object = getattr(self, feature)(network_traffic)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(
            network_object, network_traffic
        )
        observable['misp_object'] = misp_object
        for asset in ('src', 'dst'):
            if hasattr(network_traffic, f'{asset}_ref'):
                referenced_object = self.main_parser._observable[
                    getattr(network_traffic, f'{asset}_ref')
                ]
                content = super()._parse_network_traffic_reference_observable(
                    asset, referenced_object['observable']
                )
                for *attribute, kwargs in content:
                    misp_object.add_attribute(*attribute, **kwargs)
                referenced_object['used'][self.event_uuid] = True
                referenced_object['misp_object'] = misp_object
        if hasattr(network_traffic, 'encapsulates_refs'):
            for reference in network_traffic.encapsulates_refs:
                referenced = self._parse_network_traffic_observable_object(
                    reference
                )
                misp_object.add_reference(referenced.uuid, 'encapsulates')
        if hasattr(network_traffic, 'encapsulated_by_ref'):
            referenced = self._parse_network_traffic_observable_object(
                network_traffic.encapsulated_by_ref
            )
            misp_object.add_reference(referenced.uuid, 'encapsulated-by')
        return misp_object

    @staticmethod
    def _parse_network_traffic_observable_fields(
            observable: NetworkTraffic) -> str:
        if getattr(observable, 'extensions', {}).get('socket-ext'):
            return '_parse_network_socket_observable_object'
        return '_parse_network_connection_observable_object'

    def _parse_process_observable_object(self, process_ref: str) -> MISPObject:
        observable = self.main_parser._observable[process_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_object']
        process = observable['observable']
        process_object = self._create_misp_object_from_observable_object(
            'process', process
        )
        for attribute in super()._parse_process_observable(process):
            process_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(process_object, process)
        observable['misp_object'] = misp_object
        if hasattr(process, 'opened_connection_refs'):
            for reference in process.opened_connection_refs:
                network_object = self._parse_network_traffic_observable_object(
                    reference
                )
                misp_object.add_reference(
                    network_object.uuid, 'opens-connection'
                )
        if hasattr(process, 'creator_user_ref'):
            user_object = self._parse_user_account_observable_object(
                process.creator_user_ref
            )
            user_object.add_reference(misp_object.uuid, 'creates')
        if hasattr(process, 'image_ref'):
            file_object = self._parse_file_observable_object(process.image_ref)
            misp_object.add_reference(file_object.uuid, 'executes')
        if hasattr(process, 'parent_ref'):
            parent_object = self._parse_process_observable_object(
                process.parent_ref
            )
            parent_object.add_reference(misp_object.uuid, 'parent-of')
        if hasattr(process, 'child_refs'):
            for reference in process.child_refs:
                child_object = self._parse_process_observable_object(reference)
                child_object.add_reference(misp_object.uuid, 'child-of')
        return misp_object

    def _parse_registry_key_observable_object(self, registry_key_ref: str):
        observable = self.main_parser._observable[registry_key_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_object']
        registry_key = observable['observable']
        registry_key_object = self._create_misp_object_from_observable_object(
            'registry-key', registry_key
        )
        for attribute in super()._parse_registry_key_observable(registry_key):
            registry_key_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(
            registry_key_object, registry_key
        )
        observable['misp_object'] = misp_object
        if len(registry_key.get('values', [])) > 1:
            object_id = registry_key.id
            for index, registry_key_value in enumerate(registry_key['values']):
                value_object = self._create_misp_object('registry-key-value')
                value_object.from_dict(
                    uuid=self._create_v5_uuid(
                        f'{object_id} - values - {index}'
                    ),
                    comment=f'Original Windows Registry Key ID: {object_id}'
                )
                attributes = super()._parse_registry_key_value_observable(
                    registry_key_value, value_object.uuid
                )
                for attribute in attributes:
                    value_object.add_attribute(**attribute)
                misp_object.add_reference(value_object.uuid, 'contains')
                self.main_parser._add_misp_object(value_object, registry_key)
        return misp_object

    def _parse_software_observable_object(
            self, software_ref: str) -> MISPObject:
        observable = self.main_parser._observable[software_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_object']
        software = observable['observable']
        software_object = self._create_misp_object_from_observable_object(
            'software', software
        )
        for attribute in super()._parse_software_observable(software):
            software_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(
            software_object, software
        )
        observable['misp_object'] = misp_object
        return misp_object

    def _parse_url_observable_object(self, url_ref: str) -> MISPAttribute:
        observable = self.main_parser._observable[url_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_attribute']
        url = observable['observable']
        misp_attribute = self.main_parser._add_misp_attribute(
            self._create_misp_attribute('url', url), url
        )
        observable['used'][self.event_uuid] = True
        observable['misp_attribute'] = misp_attribute
        return misp_attribute

    def _parse_user_account_observable_object(
            self, user_account_ref: str) -> MISPObject:
        observable = self.main_parser._observable[user_account_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_object']
        user_account = observable['observable']
        user_account_object = self._create_misp_object_from_observable_object(
            'user-account', user_account
        )
        for attribute in super()._parse_user_account_observable(user_account):
            user_account_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(
            user_account_object, user_account
        )
        observable['misp_object'] = misp_object
        return misp_object

    def _parse_x509_observable_object(self, x509_ref: str) -> MISPObject:
        observable = self.main_parser._observable[x509_ref]
        if observable['used'].get(self.event_uuid, False):
            return observable['misp_object']
        x509 = observable['observable']
        x509_object = self._create_misp_object_from_observable_object(
            'x509', x509
        )
        for attribute in super()._parse_x509_observable(x509):
            x509_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(x509_object, x509)
        observable['misp_object'] = misp_object
        return misp_object


class STIX2SampleObservableConverter(
        STIX2ObservableConverter, metaclass=ABCMeta):
    def __init__(self, main: _MAIN_CONVERTER_TYPING):
        self._main_converter = main

    @property
    def event_uuid(self) -> str:
        return self.main_parser.misp_event.uuid

    @property
    def main_parser(self) -> 'ExternalSTIX2toMISPParser':
        return self._main_converter.main_parser

    def _create_misp_object_from_observable(
            self, name: str, observable: _OBSERVABLE_TYPING,
            malware: Malware) -> MISPObject:
        misp_object = MISPObject(
            name, force_timestamps=True,
            misp_objects_path_custom=_MISP_OBJECTS_PATH
        )
        self.main_parser._sanitise_object_uuid(
            misp_object, observable.get('id')
        )
        misp_object.from_dict(**self._main_converter._parse_timeline(malware))
        return misp_object

    def _parse_artifact_observable_object(
            self, artifact_ref: str, malware: Malware) -> MISPObject:
        observable = self.main_parser._observable[artifact_ref]
        if observable['used'][self.event_uuid]:
            return observable['misp_object']
        artifact = observable['observable']
        artifact_object = self._create_misp_object_from_observable(
            'artifact', artifact, malware
        )
        for attribute in super()._parse_artifact_observable(artifact):
            artifact_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self._main_parser._add_misp_object(
            artifact_object, artifact
        )
        observable['misp_object'] = misp_object
        return misp_object

    def _parse_file_observable_object(
            self, file_ref: str, malware: Malware) -> MISPObject:
        observable = self.main_parser._observable[file_ref]
        if observable['used'][self.event_uuid]:
            return observable['misp_object']
        _file = observable['observable']
        file_object = self._create_misp_object_from_observable(
            'file', _file, malware
        )
        for attribute in super()._parse_file_observable(_file):
            file_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(file_object, _file)
        observable['misp_object'] = misp_object
        return misp_object

    def _parse_software_observable_object(
            self, software_ref: str, malware: Malware) -> MISPObject:
        observable = self.main_parser._observable[software_ref]
        if observable['used'][self.event_uuid]:
            return observable['misp_object']
        software = observable['observable']
        software_object = self._create_misp_object_from_observable(
            'software', software, malware
        )
        for attribute in super()._parse_software_observable(software):
            software_object.add_attribute(**attribute)
        observable['used'][self.event_uuid] = True
        misp_object = self.main_parser._add_misp_object(
            software_object, software
        )
        observable['misp_object'] = misp_object
        return misp_object


class ExternalSTIX2SampleObservableConverter(STIX2SampleObservableConverter):
    def __init__(self, main: 'ExternalSTIX2MalwareConverter'):
        super().__init__(main)
        self._mapping = ExternalSTIX2ObservableMapping


class InternalSTIX2SampleObservableConverter(STIX2SampleObservableConverter):
    def __init__(self, main: 'InternalSTIX2MalwareConverter'):
        super().__init__(main)
        self._mapping = InternalSTIX2ObservableMapping
