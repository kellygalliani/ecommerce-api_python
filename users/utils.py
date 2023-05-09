from uuid import UUID

def is_valid_uuid(uuid_to_test: str):
        try:
            UUID(uuid_to_test)
            return True
        except ValueError:
            return False