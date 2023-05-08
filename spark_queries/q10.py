from spark_queries import utils

Q_NUM = 10


def q():
    query_str = f"""
    select
        c_custkey,
        c_name,
        round(sum(l_extendedprice * (1 - l_discount)), 2) as revenue,
        c_acctbal,
        n_name,
        c_address,
        c_phone,
        c_comment
    from
        customer,
        orders,
        lineitem,
        nation
    where
        c_custkey = o_custkey
        and l_orderkey = o_orderkey
        and o_orderdate >= date '1993-10-01'
        and o_orderdate < date '1993-10-01' + interval '3' month
        and l_returnflag = 'R'
        and c_nationkey = n_nationkey
    group by
        c_custkey,
        c_name,
        c_acctbal,
        c_phone,
        n_name,
        c_address,
        c_comment
    order by
        revenue desc
    limit 20
	"""

    utils.get_customer_ds()
    utils.get_orders_ds()
    utils.get_line_item_ds()
    utils.get_nation_ds()

    q_final = utils.get_or_create_spark().sql(query_str)

    q_final.show()

    utils.run_query(Q_NUM, q_final)


if __name__ == "__main__":
    q()
