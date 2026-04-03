from data_service import MemberMockDataService

class MemberService:
    def __init__(self):
        self.data_service = MemberMockDataService()

    def get_all(self):
        return self.data_service.get_all_members()

    def get_by_id(self, member_id):
        return self.data_service.get_member_by_id(member_id)

    def create(self, data):
        return self.data_service.add_member(data)

    def update(self, member_id, data):
        return self.data_service.update_member(member_id, data)

    def delete(self, member_id):
        return self.data_service.delete_member(member_id)