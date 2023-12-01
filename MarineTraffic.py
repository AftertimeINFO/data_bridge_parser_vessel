# region Standard libraries
import signal
import time
import sys
from datetime import datetime
# endregion

# region External libraries
# endregion

# region Project internal libraries
from mt_operations.map.mt_map_operations import MapOperationsList
# endregion




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def write_log(comment):
    with open('log.txt', 'a') as f:
        f.write(f'\n{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {comment}')

def handler(signum, frame):
    raise StopIteration("BREAK")

def run_parser(start_parsing: bool, trace_name: str = None):
    write_log(f'----------------Run script on {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}----------------')
    MOL = MapOperationsList()
    try:

        def list_operation():
            MOL.initialize(full=False, reload=False)
            list_id = 1
            for cur_step in MOL.inter_one_passage:
                print(f"{list_id}:", cur_step.get_dict())
                list_id += 1

        input_data = ""
        if start_parsing is True:
            input_data="s"

        while input_data != "e" and input_data != "s":
            input_data = input("(s-start, sv-save, b-back, r-repeat, zi/zo-zoom in/out,"
                               "l-list,  a-append, cr-Coordinates renew, e-exit):")

            if input_data == "l":
                list_operation()
            elif input_data == 'sv':
                MOL.save_trace()
            elif input_data == 'cr':
                MOL.initialize(full=True, reload=False)
                i = 1
                for cur_step in MOL.inter_renew:
                    print(f"operation {i}")
                    cur_step.execute()
                    i += 1
                    # print(f"{list_id}:", cur_step.get_dict())
                    # list_id += 1
            elif input_data == "a":
                input_second = ""
                while input_second != "g":
                    list_operation()
                    input_second = input("Select Type of operation (g-go back, sv-save, "
                                         "0-Initialization, 1-Move, 6-clear vehicles)")

                    if input_second == '1':
                        try:
                            input_operation = input("Movement x,y:")
                            (x, y) = input_operation.split(",")
                            check = input("Make check (yes,no) [no-default]:")
                            if check.lstrip("w.") == "":
                                check = 0
                            elif check == "yes":
                                check = True
                            elif check == "no":
                                check = False

                            MOL.append_operation(operation_type=int(input_second), x=int(x), y=int(y), checking=check)
                        except BaseException as e:
                            print(bcolors.WARNING + "Incorrect data format."+ bcolors.ENDC)
                            time.sleep(5)
                    elif input_second == '6':
                        try:
                            input_operation = input("Direction (1-front,-1-back) [1-default]:")
                            if input_operation.lstrip("w.") == "":
                                direction = 1
                            else:
                                direction = int(input_operation)

                            MOL.append_operation(operation_type=int(input_second), direction_condition=direction)
                        except BaseException as e:
                            print(bcolors.WARNING + "Incorrect input." + bcolors.ENDC)
                            time.sleep(5)
                    elif input_second == 'sv':
                        MOL.save_trace()

        if input_data == "s":

            end_less_circle = True

            signal.signal(signal.SIGINT, handler)
            while end_less_circle:
                try:
                    MOL.initialize(trace_name=trace_name)

                    for cur_step in MOL:
                        print("Operation type: ", cur_step.structure["operation_type"])
                        if cur_step.structure["operation_type"] == 0:
                            pass
                        cur_step.execute()

                except StopIteration as e:
                    MOL.close_driver()
                    break
                except BaseException as e:
                    error_message = f"Error: {e}"
                    print(error_message)
                    write_log(error_message)
                    MOL.close_driver()


    except BaseException as e:
        print("Exception: ", e)
    finally:
        MOL.close_driver()
        print(f'----------------End script on {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}----------------)')


if __name__ == '__main__':
    start_parsing = False
    trace_name = None
    if len(sys.argv) > 1:
        arg_length = len(sys.argv)

        for cur_arg_id in range(1, arg_length) :
            cur_arg = sys.argv[cur_arg_id]
            if cur_arg == "--start":
                start_parsing=True
            elif cur_arg == "--trace":
                try:
                    cur_arg_id += 1
                    trace_name = sys.argv[cur_arg_id]
                except BaseException as e:
                    raise Exception("Incorrect TRACE parameter")
    run_parser(start_parsing=start_parsing, trace_name=trace_name)
