from fastapi import APIRouter
from sqlalchemy import text

from customfunctions import generate_zero_for_missing_hours_in_day_query
from db import DW

router = APIRouter(
    prefix='/api/measurement/temperature',
    tags=['Temperature']
)


# Haetaan annetun päivän keskiarvolämpötilat, jotka lajitellaan
# tuntikohtaisesti.
@router.get("/avg/hourly/{date}")
async def get_avg_temperature_statistics_hourly_by_day(dw: DW, date: str):
    """
    Get hourly temperatures (avg) from a given day.
    String ISO 8601 format YYYY-MM-DD.
    """
    _query = text("SELECT DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) as date, "
                  "d.hour, avg(value) AS temperature "
                  "FROM temperatures_fact t "
                  "JOIN dates_dim d ON t.date_key = d.date_key "
                  "WHERE DATE(TIMESTAMP(CONCAT_WS('-', d.year, d.month, d.day))) = DATE(:date) "
                  "GROUP BY d.hour "
                  "ORDER BY d.hour;")
    rows = dw.execute(_query, {"date": date})
    fetched_data = rows.mappings().all()

    data = generate_zero_for_missing_hours_in_day_query(fetched_data)

    return {"data": data}
