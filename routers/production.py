from fastapi import APIRouter
from sqlalchemy import text
from db import DW


router = APIRouter(
    prefix='/api/measurement/production',
    tags=['Production']
)


# Haetaan päiväkohtainen kokonaistuotto tunneittain ryhmiteltynä:
# Tämä on total production chartin DAY nappia varten.
@router.get("/total/hourly_for_day/{date}")
async def get_total_production_statistics_hourly_for_a_day(dw: DW, date: str):
    """
    Get production stats from a given day grouped by hour. String format YYYY-MM-DD
    """
    _query = text("SELECT SUM(p.value) AS total_production, d.hour "
                  "FROM productions_fact p JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE CONCAT_WS('-', d.year, d.month, d.day) = DATE(:date) "
                  "GROUP BY d.hour;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan päiväkohtainen kokonaistuotto.
# Tämä on total production screenin DAY-näkymän Total-kohtaa varten.
@router.get("/total/day/{date}")
async def get_total_production_statistics_for_a_day(dw: DW, date: str):
    """
    Get production stats from a given day. String format YYYY-MM-DD
    """
    _query = text("SELECT DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) as day, "
                  "SUM(p.value) AS total_production "
                  "FROM productions_fact p JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE CONCAT_WS('-', d.year, d.month, d.day) = DATE(:date);")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan kaikelle tuotolle päiväkohtainen keskiarvo:
# Tämä on total production screenin DAY-näkymän Avg-kohtaa varten.
@router.get("/avg/day/{date}")
async def get_avg_production_statistics_for_a_day(dw: DW, date: str):
    """
    Get production stats from a given day. String format YYYY-MM-DD
    """
    _query = text("SELECT DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) as day, "
                  "AVG(p.value) AS avg_production "
                  "FROM productions_fact p JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE CONCAT_WS('-', d.year, d.month, d.day) = DATE(:date);")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan viikkokohtainen kokonaistuotto päivittäin ryhmiteltynä.
# Tämä on total production chartin WEEK nappia varten.
@router.get("/total/daily_for_week/{date}")
async def get_total_production_statistics_daily_for_a_week(dw: DW, date: str):
    """
    Get production stats from a given week grouped by day. String format YYYY-MM-DD
    """
    _query = text("SELECT DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) as day, "
                  "SUM(p.value) AS total_production FROM productions_fact p "
                  "JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) "
                  "BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND :date "
                  "GROUP BY d.day;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan viikkokohtainen kokonaistuotto:
# Tämä on total production screenin WEEK-näkymän Total-kohtaa varten.
@router.get("/total/week/{date}")
async def get_total_production_statistics_for_a_week(dw: DW, date: str):
    """
    Get production stats from a given week. String format YYYY-MM-DD
    """
    _query = text("SELECT SUM(p.value) AS total_production "
                  "FROM productions_fact p "
                  "JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) "
                  "BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND :date;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan viikkokohtainen keskiarvotuotto:
# Tämä on total production screenin WEEK-näkymän Avg-kohtaa varten.
@router.get("/avg/week/{date}")
async def get_avg_production_statistics_for_a_week(dw: DW, date: str):
    """
    Get production stats from a given week. String format YYYY-MM-DD
    """
    _query = text("SELECT AVG(p.value) AS total_production "
                  "FROM productions_fact p "
                  "JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) "
                  "BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND :date;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan kuukausikohtainen kokonaistuotto päivittäin ryhmiteltynä:
# Tämä on total production chartin MONTH nappia varten.
@router.get("/total/daily_for_month/{date}")
async def get_total_production_statistics_daily_for_a_month(dw: DW, date: str):
    """
    Get production stats from a given month grouped by day. String format YYYY-MM-DD
    """
    _query = text("SELECT DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) as day, "
                  "SUM(p.value) AS total_production FROM productions_fact p "
                  "JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) "
                  "BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND :date "
                  "GROUP BY d.day;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan kuukausikohtainen kokonaistuotto.
# Tämä on total production screenin MONTH-näkymän Total-kohtaa varten.
@router.get("/total/month/{date}")
async def get_total_production_statistics_for_a_month(dw: DW, date: str):
    """
    Get production stats from a given month. String format YYYY-MM-DD
    """
    _query = text("SELECT SUM(p.value) AS total_production "
                  "FROM productions_fact p "
                  "JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) "
                  "BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND :date;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan kuukausikohtainen keskiarvotuotto.
# Tämä on total production screenin MONTH-näkymän Avg-kohtaa varten.
@router.get("/avg/month/{date}")
async def get_avg_production_statistics_for_a_month(dw: DW, date: str):
    """
    Get production stats from a given month. String format YYYY-MM-DD
    """
    _query = text("SELECT AVG(p.value) AS total_production "
                  "FROM productions_fact p "
                  "JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) "
                  "BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND :date;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan vuosikohtainen kokonaistuotto kuukausittain ryhmiteltynä.
# Tämä on total production chartin YEAR nappia varten.
@router.get("/total/monthly_for_year/{date}")
async def get_total_production_statistics_monthly_for_a_year(dw: DW, date: str):
    """
    Get production stats from a given year grouped by month. String format YYYY-MM-DD
    """
    _query = text("SELECT CONCAT_WS('-', d.year, d.month) AS year_and_month, "
                  "SUM(p.value) AS total_production "
                  "FROM productions_fact p "
                  "JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) "
                  "BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND :date "
                  "GROUP BY d.month;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan vuosikohtainen kokonaistuotto.
# Tämä on total production screenin YEAR-näkymän Total-kohtaa varten.
@router.get("/total/year/{date}")
async def get_total_production_statistics_for_a_year(dw: DW, date: str):
    """
    Get production stats from a given year. String format YYYY-MM-DD
    """
    _query = text("SELECT SUM(p.value) AS total_production FROM productions_fact p "
                  "JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) "
                  "BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND :date;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}


# Haetaan vuosikohtainen keskiarvotuotto.
# Tämä on total production screenin YEAR-näkymän Avg-kohtaa varten.
@router.get("/avg/year/{date}")
async def get_avg_production_statistics_for_a_year(dw: DW, date: str):
    """
    Get production stats from a given year. String format YYYY-MM-DD
    """
    _query = text("SELECT AVG(p.value) AS total_production FROM productions_fact p "
                  "JOIN dates_dim d ON p.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) "
                  "BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND :date;")
    rows = dw.execute(_query, {"date": date})
    data = rows.mappings().all()
    return {"data": data}

