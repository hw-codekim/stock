import streamlit as st


class dbData:
    def stock_semi():
        conn = st.connection("mydb", type="sql", autocommit=True)
        df = conn.query(
            """
            SELECT sp.날짜,섹터,count(종목) 종목수,sum(거래대금)합계,round(avg(등락률),1) 등락률
            FROM stock_price sp 
                JOIN (SELECT * FROM stock_information)si
                ON si.기업명 = sp.종목 
            WHERE 섹터 = '석유와가스'
            GROUP BY 날짜
            ORDER BY 날짜 DESC 
            """)
        return df

    def get_finance():
        conn = st.connection("mydb", type="sql", autocommit=True)
        df = conn.query(
           f"""
            SELECT *
            FROM finance 
            """)
        return df