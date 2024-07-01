
import plotnine as p9
from matplotlib import pyplot as plt
import pandas as pd
import database.db_operation
from sqlalchemy import create_engine
import pytz

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

    # todo : sensor 2

    # data from databas
    measurements_temperature_1_df = database.db_operation.read_temperature_df_from_measurements(engine = sqlengine, node_id = 10, sensortype = 1, limit = 25)
    # convert unix time to datetime
    timezone = pytz.timezone('Etc/GMT-2') 
    measurements_temperature_1_df['time'] = pd.to_datetime(measurements_temperature_1_df['time_unix_s'], unit='s', utc=True)
    measurements_temperature_1_df['time'] = measurements_temperature_1_df['time'].dt.tz_convert(timezone)
    print(measurements_temperature_1_df.head())
    # 
    min_time = measurements_temperature_1_df['time'].min().floor('30S')
    max_time = measurements_temperature_1_df['time'].max().ceil('30S')


    if measurements_temperature_1_df.empty:
        print(f"Empty data frame")
        return

    plot_temperature = (
        p9.ggplot(
           measurements_temperature_1_df,
           p9.aes(
               x="time",
               y="sensor_value",
               color="factor(sensortype)"  # Optional: add color by node_id
           ),
        )
        + p9.geom_line(linetype="none")
        + p9.geom_point()
        + p9.labs(
           title="Temperature Measurements",
           x="Time",
           y="Temperature (°C)",
           color="Sensor"
        )
        + p9.theme_minimal()
        + p9.scale_y_continuous(limits = [20, 30], breaks=range(10, 31, 1))
        + p9.scale_x_datetime(
            date_labels="%H:%M:%S",
            breaks=pd.date_range(
                #start=measurements_temperature_1_df['time'].min()
                #end=measurements_temperature_1_df['time'].max()
                start=min_time,
                end=max_time,
                freq='30S'
            )
        )
        + p9.theme(
            axis_text_x=p9.element_text(angle=45, hjust=1)
        )
    )
    # plt.ion()
    #plot_temperature.show()
    plot_temperature.save("temperature_plot.png")
    
    return None


    # ===========================================
    # DOES NOT WORK
    # # Plot with matplotlib
    # fig, ax = plt.subplots()

    # # Plot lines and points for the filtered node_id
    # ax.plot(measurements_temperature_df['time'], measurements_temperature_df['sensor_value'], linestyle='--', color='blue')
    # ax.scatter(measurements_temperature_df['time'], measurements_temperature_df['sensor_value'], color='blue')

    # # Set labels and title
    # ax.set_title('Temperature Measurements')
    # ax.set_xlabel('Time')
    # ax.set_ylabel('Temperature (°C)')

    # # Add a legend
    # #ax.legend(title='Node ID')

    # # Apply minimal theme-like style
    # ax.grid(True, linestyle='--', linewidth=0.5)
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)

    # #
    # plt.xticks(rotation=45)
    # plt.tight_layout()

    # # Show the plot
    # plt.ion()
    # #plt.draw()
    # plt.show()
    # plt.pause(0.001)

    # return None
