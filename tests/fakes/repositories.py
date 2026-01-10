from typing import List, Optional
from src.domain.entities import Contact, Lead, Operator, OperatorSource


class FakeOperatorRepository:
    def __init__(self) -> None:
        self._operators: dict[int, Operator] = dict()
        self._id_counter = 1

    def add(self, entity: Operator) -> Operator:
        entity.id = self._id_counter
        self._operators[entity.id] = entity
        self._id_counter += 1
        return entity

    def get_by_id(self, id: int) -> Optional[Operator]:
        return self._operators.get(id)

    def get_all(self) -> List[Operator]:
        return list(self._operators.values())

    def get_sorted_list_by_filter(self,
        filter_arg: str,
        only_acceptable: bool = True,
        reverse: bool = True
    ) -> List[Operator]:
        """
        Args:
            filter_arg: str - key for filter
            only_acceptable: bool = True - show only acceptable operators
            reverse: bool = True - by default ascending
        Return:
            List[Operator]
        """
        if only_acceptable:
            return list(
                op for op in sorted(
                    self._operators.values(),
                    key=lambda x: x.filter_arg,
                    reverse=reverse
                ) if op.can_accept_lead()
            )

        return list(
             op for op in sorted(
                self._operators.values(),
                key=lambda x: x.filter_arg,
                reverse=reverse
                )
        )

    def get_one_operator_by_filter(
        self,
        filter_arg: str,
        only_acceptable: bool = True,
        reverse: bool = True,
    ) -> Operator:
        """
        Args:
            filter_arg: str - key for filter
            only_acceptable: bool = True - show only acceptable operators
            reverse: bool = True - by default ascending
        Return:
            domain.entities.Operator()
        """
        return self.get_sorted_list_by_filter(
            filter_arg,
            only_acceptable,
            reverse
        )[0]


class FakeLeadRepository:
    def __init__(self) -> None:
        self._leads: dict[int, Lead] = dict()
        self._id_counter = 1

    def add(self, entity: Lead) -> Lead:
        entity.id = self._id_counter
        self._leads[entity.id] = entity
        self._id_counter += 1
        return entity

    def get_by_id(self, id: int) -> Optional[Lead]:
        return self._leads.get(id)

    def get_by_external_id(
        self,
        external_id: int
    ) -> Optional[Lead]:
        for _, lead in self._leads.items():
            if lead.external_id == external_id:
                return lead

    def get_all(self) -> List[Lead]:
        return list(self._leads.values())


class FakeSourceRepository:
    def __init__(self) -> None:
        self._sources: dict[int, OperatorSource] = dict()
        self._id_counter = 1

    def add(self, entity: OperatorSource) -> OperatorSource:
        entity.id = self._id_counter
        self._sources[entity.id] = entity
        self._id_counter += 1
        return entity

    def get_by_id(self, id: int) -> Optional[OperatorSource]:
        return self._sources.get(id)

    def get_all(self) -> List[OperatorSource]:
        return list(self._sources.values())


class FakeContactRepository:
    def __init__(self) -> None:
        self._contacts: dict[int, Contact] = dict()
        self._id_counter = 1

    def add(self, entity: Contact) -> Contact:
        entity.id = self._id_counter
        self._contacts[entity.id] = entity
        self._id_counter += 1
        return entity

    def get_by_id(self, id: int) -> Optional[Contact]:
        return self._contacts.get(id)

    def get_all(self) -> List[Contact]:
        return list(self._contacts.values())

    def get_by_lead_id(self, lead_id: int) -> List[Contact]:
        return [c for c in self._contacts.values() if c.lead_id == lead_id]

    def get_by_operator_id(self, operator_id: int) -> List[Contact]:
        return [c for c in self._contacts.values() if c.operator_id == operator_id]



class FakeOperatorSourceRepository:
    def __init__(self) -> None:
        self._items: List[OperatorSource] = list()

    def add(self, entity: OperatorSource) -> OperatorSource:
        self._items.append(entity)
        return entity

    def get_all(self) -> List[OperatorSource]:
        return self._items.copy()

    def get_by_source_id(self, source_id: int) -> List[OperatorSource]:
        return [os for os in self._items if os.source_id == source_id]
