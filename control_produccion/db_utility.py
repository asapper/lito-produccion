import datetime
import psycopg2

from django.db import DatabaseError
from django.utils import timezone

from .models import ProcessState


# constants
VAL_INDEX = 0
VAL_VALUE = 1

# indeces of rows read
INDEX_ORDER_DB_ID = 0
INDEX_PRODUCT_ID = 1
INDEX_PROCESS_GROUP = 2
INDEX_PROCESS_ID = 3
INDEX_PROCESS_NAME = 4
INDEX_CLIENT = 5
INDEX_OP_NUMBER = 6
INDEX_QUANTITY = 7
INDEX_SHEETS = 8
INDEX_DESCRIPTION = 9
INDEX_PRODUCT_NAME = 10
INDEX_DATE_CREATED = 11
INDEX_DUE_DATE = 12

# values of stored indices
VALUE_ORDER_DB_ID = 'order_db_id'
VALUE_PRODUCT_ID = 'product_id'
VALUE_PROCESS_GROUP = 'process_group'
VALUE_PROCESS_ID = 'process_id'
VALUE_PROCESS_NAME = 'process_name'
VALUE_CLIENT = 'client'
VALUE_OP_NUMBER = 'op_number'
VALUE_QUANTITY = 'quantity'
VALUE_SHEETS = 'sheets'
VALUE_DESCRIPTION = 'description'
VALUE_PRODUCT_NAME = 'product'
VALUE_DATE_CREATED = 'date_created'
VALUE_DUE_DATE = 'due_date'

# list of tuples of index, name-of-field
INDICES = [
    (INDEX_ORDER_DB_ID, VALUE_ORDER_DB_ID),  # index 0
    (INDEX_PRODUCT_ID, VALUE_PRODUCT_ID),  # index 1
    (INDEX_PROCESS_GROUP, VALUE_PROCESS_GROUP),  # index 2
    (INDEX_PROCESS_ID, VALUE_PROCESS_ID),  # index 3
    (INDEX_PROCESS_NAME, VALUE_PROCESS_NAME),  # index 4
    (INDEX_CLIENT, VALUE_CLIENT),  # index 5
    (INDEX_OP_NUMBER, VALUE_OP_NUMBER),  # index 6
    (INDEX_QUANTITY, VALUE_QUANTITY),  # index 7
    (INDEX_SHEETS, VALUE_SHEETS),  # index 8
    (INDEX_DESCRIPTION, VALUE_DESCRIPTION),  # index 9
    (INDEX_PRODUCT_NAME, VALUE_PRODUCT_NAME),  # index 10
    (INDEX_DATE_CREATED, VALUE_DATE_CREATED),  # index 11
    (INDEX_DUE_DATE, VALUE_DUE_DATE),  # index 12
]

# db info
DB_NAME = "sunhive"
DB_USER = "reportecl"
DB_PSSWD = "clitografica16"
DB_HOST = "192.168.0.20"
DB_PORT = "5432"

# process query
PROCESS_QUERY = (
    "select \"FechaInicio\", \"FechaFin\" from "
    "\"Produccion\".\"Tiempos\" "
    "where \"CodigoOrdenProduccion\" = {} and "  # Codigo de la orden
    "\"LineaProducto\" = {} and "  # Linea del producto, si es portada o interiores
    "\"CodigoProceso\" = {} and "  # Codigo del proceso
    "\"LineaProcesoOrdenProduccion\"  = {} "  # codigo/linea del subproceso
    "order by \"FechaInicio\" ")

# main query
MAIN_QUERY = (
    "select qr.*, op.\"NombreCliente\", op.\"Numero\", opp.\"Cantidad\", opm.\"NumeroPliegosPrensa\" + opm.\"VentajaPliegosPrensa\" as \"TotalPliegosPrensa\", opp.\"DescripcionProducto\",op.\"Descripcion\", op.\"FechaCreacion\", op.\"FechaRequerida\" "
    "from ( "
    "select \"CodigoOrdenProduccion\", \"Linea\" as \"LineaProducto\", 1 as \"CodigoProceso\", -1 as \"LineaProceso\", 'CORTE INICIAL' AS \"Proceso\" "
    "from \"Produccion\".\"OrdenesProduccionCorte\" opo "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=opo.\"CodigoOrdenProduccion\" "
    "where  "
    "op.\"Estado\" in ('P','R') "
    "and op.\"FechaCreacion\" > '{0}' "
    "union "
    "select \"CodigoOrdenProduccion\", \"Linea\" as \"LineaProducto\", 1 as \"CodigoProceso\", 0 as \"LineaProceso\", 'CORTE FINAL' AS \"Proceso\" "
    "from \"Produccion\".\"OrdenesProduccionCorte\" opo "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=opo.\"CodigoOrdenProduccion\" "
    "where  "
    "op.\"Estado\" in ('P','R') "
    "and op.\"FechaCreacion\" > '{0}' "
    "union "
    "select \"CodigoOrdenProduccion\", \"Linea\" as \"LineaProducto\", 2 as \"CodigoProceso\", -1 as \"LineaProceso\", 'OFFSET' as \"Proceso\" "
    "from \"Produccion\".\"OrdenesProduccionOffset\" opo "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=opo.\"CodigoOrdenProduccion\" "
    "where  "
    "op.\"Estado\" in ('P','R') "
    "and op.\"FechaCreacion\" > '{0}' "
    "union "
    "select \"CodigoOrdenProduccion\", \"Linea\" as \"LineaProducto\", 3 as \"CodigoProceso\", -1 as \"LineaProceso\", 'BARNIZADO' AS \"Proceso\" "
    "from \"Produccion\".\"OrdenesProduccionBarniz\" opo "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=opo.\"CodigoOrdenProduccion\" "
    "where  "
    "op.\"Estado\" in ('P','R') "
    "and op.\"FechaCreacion\" > '{0}' "
    "union "
    "select \"CodigoOrdenProduccion\", \"Linea\" as \"LineaProducto\", 4 as \"CodigoProceso\", \"LineaTipografia\" as \"LineaProceso\", mt.\"Descripcion\" AS \"Proceso\" "
    "from \"Produccion\".\"OrdenesProduccionTipografia\" opt "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=opt.\"CodigoOrdenProduccion\" "
    "INNER JOIN \"Cotizaciones\".\"MaquinasTipografia\" mt on "
    "mt.\"Codigo\"=opt.\"CodigoMaquinaTipografia\" "
    "where  "
    "op.\"Estado\" in ('P','R') "
    "and op.\"FechaCreacion\" > '{0}' "
    "union "
    "select \"CodigoOrdenProduccion\", \"Linea\" as \"LineaProducto\", 5 as \"CodigoProceso\", -1 as \"LineaProceso\", 'DOBLADO' AS \"Proceso\" "
    "from \"Produccion\".\"OrdenesProduccionDoblado\" opo "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=opo.\"CodigoOrdenProduccion\" "
    "where  "
    "op.\"Estado\" in ('P','R') "
    "and op.\"FechaCreacion\" > '{0}' "
    "union "
    "select \"CodigoOrdenProduccion\", \"Linea\" as \"LineaProducto\", 6 as \"CodigoProceso\", -1 as \"LineaProceso\", 'COMPAGINADO' AS \"Proceso\" "
    "from \"Produccion\".\"OrdenesProduccionCompaginado\" opo "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=opo.\"CodigoOrdenProduccion\" "
    "where  "
    "op.\"Estado\" in ('P','R') "
    "and op.\"FechaCreacion\" > '{0}' "
    "union "
    "select \"CodigoOrdenProduccion\", \"Linea\" as \"LineaProducto\", 7 as \"CodigoProceso\", \"LineaEmpaque\" as \"LineaProceso\", pe.\"Descripcion\" AS \"Proceso\" "
    "from \"Produccion\".\"OrdenesProduccionEmpaque\" ope "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=ope.\"CodigoOrdenProduccion\" "
    "INNER JOIN \"Cotizaciones\".\"ProcesosEmpaque\" pe on "
    "pe.\"Codigo\"=ope.\"CodigoProcesoEmpaque\" "
    "where  "
    "op.\"Estado\" in ('P','R') "
    "and op.\"FechaCreacion\" > '{0}'  "
    "union "
    "select \"CodigoOrdenProduccion\", \"Linea\" as \"LineaProducto\", 8 as \"CodigoProceso\", \"LineaProceso\" as \"LineaProceso\", opo.\"Descripcion\" AS \"Proceso\" "
    "from \"Produccion\".\"OrdenesProduccionOtrosProcesos\" opo "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=opo.\"CodigoOrdenProduccion\"  "
    "where  "
    "op.\"Estado\" in ('P','R') "
    "and op.\"FechaCreacion\" > '{0}'  "
    ") qr "
    "inner join \"Produccion\".\"OrdenesProduccion\" op on "
    "op.\"Codigo\"=qr.\"CodigoOrdenProduccion\" "
    "inner join \"Produccion\".\"OrdenesProduccionProductos\" opp on "
    "opp.\"CodigoOrdenProduccion\"=op.\"Codigo\" and  "
    "opp.\"Linea\" = qr.\"LineaProducto\" "
    "inner join \"Produccion\".\"OrdenesProduccionMateriales\" opm on "
    "op.\"Codigo\" = opm.\"CodigoOrdenProduccion\" and "
    "opm.\"Linea\" = qr.\"LineaProducto\" "
    "where   op.\"Estado\" in ('P','R') "
    "order by \"CodigoOrdenProduccion\", \"LineaProducto\", \"CodigoProceso\", \"LineaProceso\" ")


class DatabaseController():
    @classmethod
    def get_orders(cls):
        """
        Initialize database and execute query to retrieve active orders.
        Return cleaned data.
        """
        cursor = cls.init_db()
        # get last month date in YYYYMMDD format
        last_month = timezone.now() - datetime.timedelta(days=31)
        last_month = last_month.strftime('%Y%m%d')
        # call helper function to execute query
        data = cls.execute_main_query(cursor, last_month)
        # return clean data
        return cls.clean_data(data)

    @classmethod
    def get_process_data(cls, op, product, group, process):
        """
        Connect to database and retrieve specific information about
        a process of the given Order.
        """
        cursor = cls.init_db()
        # call helper function to execute query
        data = cls.execute_process_query(
            cursor, op, product, group, process)
        return data


    @classmethod
    def init_db(cls):
        """Initialize the connection to the database and return a cursor."""
        try:
            # establish connection
            conn = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PSSWD,
                host=DB_HOST,
                port=DB_PORT)
            # get cursors
            cur = conn.cursor()
            return cur
        except psycopg2.OperationalError:
            raise DatabaseError

    @classmethod
    def execute_main_query(cls, cursor, limit_date):
        """Execute query to retrieve active orders from database."""
        # run main first query
        cursor.execute(MAIN_QUERY.format(limit_date))
        return cursor.fetchall()

    @classmethod
    def execute_process_query(cls, cursor, op, product, group, process):
        """
        Execute query to retrieve data about an
        Order's specific process.
        """
        # run process query
        cursor.execute(PROCESS_QUERY.format(
            op, product, group, process))
        rows = cursor.fetchall()
        # store state process
        state = ProcessState.NOT_STARTED
        if not rows:  # no times entered for process
            state = ProcessState.NOT_STARTED
        else:  # there are time entries
            for row in rows:
                if len(row) == 1:  # process being done
                    # if at least one entry indicates process not done
                    # there is no need to keep looking
                    state = ProcessState.STARTED
                    print("######## Process started: {}".format(op))
                    break
                elif len(row) == 2:  # process finished
                    # this entry indicates one finished cycle
                    # of work done on process, other cycle(s)
                    # could still have happened, so keep looking
                    state = ProcessState.FINISHED
                    print("######## Process finished: {}".format(op))
        # return state of given process
        return state

    @classmethod
    def clean_data(cls, data):
        """Clean given data. Return cleaned data."""
        orders = []  # store all orders
        for row in data:
            # store all data
            order_dict = {}
            order_dict[VALUE_ORDER_DB_ID] = row[INDEX_ORDER_DB_ID]
            order_dict[VALUE_PRODUCT_ID] = row[INDEX_PRODUCT_ID]
            order_dict[VALUE_PROCESS_GROUP] = row[INDEX_PROCESS_GROUP]
            order_dict[VALUE_PROCESS_ID] = row[INDEX_PROCESS_ID]
            order_dict[VALUE_PROCESS_NAME] = row[INDEX_PROCESS_NAME]
            order_dict[VALUE_CLIENT] = row[INDEX_CLIENT]
            order_dict[VALUE_OP_NUMBER] = row[INDEX_OP_NUMBER]
            order_dict[VALUE_QUANTITY] = row[INDEX_QUANTITY]
            order_dict[VALUE_SHEETS] = row[INDEX_SHEETS]
            order_dict[VALUE_DESCRIPTION] = row[INDEX_DESCRIPTION]
            order_dict[VALUE_PRODUCT_NAME] = row[INDEX_PRODUCT_NAME]
            order_dict[VALUE_DATE_CREATED] = row[INDEX_DATE_CREATED]
            order_dict[VALUE_DUE_DATE] = row[INDEX_DUE_DATE]
            # add dict to list of orders
            orders.append(order_dict)
        # return list of all info from given data
        return orders
