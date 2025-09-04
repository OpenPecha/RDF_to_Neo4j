from file_operation_utils import FileOperationUtils
from ttl_utils import TTLUtils
from work.parse_work import ParseWork

def pipeline(work_id):
    ttl_file = TTLUtils.get_ttl(work_id)
    work_info = ParseWork.parse_work_ttl(ttl_file, work_id)
    FileOperationUtils.write_json(data=work_info, file_name=work_id)

if __name__ == "__main__":
    work_ids = ["WA1KG12670", "WA0RK0013"]
    for work_id in work_ids:
        pipeline(work_id)