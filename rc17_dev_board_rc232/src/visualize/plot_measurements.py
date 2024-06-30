
import plotnine as p9
import pandas as pd
import database.db_operation

# todo : duplication
DB_FILEPATH = r"gateway_v2.db"

sqlengine = create_engine(f'sqlite:///{DB_FILEPATH}', echo=False)

def plot_measurements():
    # test data
    #measurements_temperature = {
    #    'time_unix_s': [1609459200, 1609462800, 1609466400, 1609470000],
    #    'sensor_value': [23.5, 24.0, 22.8, 23.1],
    #    'node_id': [10, 10, 10, 10]
    #}
    #measurements_temperature_df = pd.DataFrame(measurements_temperature)

    # data from database
    measurements_temperature_df = database.db_operation.read_temperature_df_from_measurements(engine = sqlengine, node_id = 10, limit = 10)
    print(measurements_temperature_df.head())
    # convert unix time to datetime
    measurements_temperature_df['time'] = pd.to_datetime(measurements_temperature_df['time_unix_s'], unit='s')

    plot_temperature = (
    p9.ggplot(
        measurements_temperature_df,
        p9.aes(
            x="time",
            y="sensor_value",
            color="factor(node_id)"  # Optional: add color by node_id
        ),
    )
    + p9.geom_line(linetype="dashed")
    + p9.geom_point()
    + p9.labs(
        title="Temperature Measurements",
        x="Time",
        y="Temperature (°C)",
        color="Node ID"
    )
    + p9.theme_minimal()
)
    plot_temperature.show()
    
    return None