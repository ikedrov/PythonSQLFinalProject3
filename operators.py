from sql_query import SqlCalls


class Calls:

    def calls_logic(self):

        SqlCalls.create_table_users()
        SqlCalls.create_table_prices()
        SqlCalls.add_users(('User1', 500))
        SqlCalls.add_prices((1, 2, 3))
        #SqlCalls.operation_report()
        SqlCalls.calls()

start = Calls()
start.calls_logic()
