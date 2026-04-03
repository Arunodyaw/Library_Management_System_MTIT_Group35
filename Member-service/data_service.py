from models import Member

class MemberMockDataService:
    def __init__(self):
        self.members = []
        self.next_id = 1

    def get_all_members(self):
        return self.members

    def get_member_by_id(self, member_id: int):
        return next((m for m in self.members if m.id == member_id), None)

    def add_member(self, data):
        new_member = Member(id=self.next_id, **data.dict())
        self.members.append(new_member)
        self.next_id += 1
        return new_member

    def update_member(self, member_id, data):
        member = self.get_member_by_id(member_id)
        if member:
            update_data = data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(member, key, value)
            return member
        return None

    def delete_member(self, member_id):
        member = self.get_member_by_id(member_id)
        if member:
            self.members.remove(member)
            return True
        return False