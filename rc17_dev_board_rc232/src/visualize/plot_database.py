
import plotnine as p9
from matplotlib import pyplot as plt
import pandas as pd
import database.db_operation
from sqlalchemy import create_engine

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
    measurements_temperature_df = database.db_operation.read_temperature_df_from_measurements(engine = sqlengine, node_id = 10, limit = 50)
    print(measurements_temperature_df.head())
    # convert unix time to datetime
    measurements_temperature_df['time'] = pd.to_datetime(measurements_temperature_df['time_unix_s'], unit='s')

    if measurements_temperature_df.empty:
        print(f"No empty data frame found")


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
    + p9.scale_y_continuous(limits = [0, 40], breaks=range(0, 41, 5))
    + p9.scale_x_datetime(date_labels="%H:%M")
    #+ p9.scale_x_datetime(breaks="1 hour", labels="%H:%M")
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
