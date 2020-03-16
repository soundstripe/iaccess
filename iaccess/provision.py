from sqlalchemy.testing.provision import temp_table_keyword_args


@temp_table_keyword_args.for_db("iaccess")
def _iseries_temp_table_keyword_args(cfg, eng):
    return {
        "prefixes": ['GLOBAL TEMPORARY'],
    }
