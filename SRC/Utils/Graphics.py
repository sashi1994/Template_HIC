import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
import plotly.express as px
import os

class Graphics:
    def __init__(self, NumberofATDs, ATD, Seat):
        """
        Initializes the Graphics class with ATD (Anthropomorphic Test Device) and Seat data.
        """
        self.ATD1 = ATD
        self.rows, self.column = self.ATD1.shape
        self.Number = int(((self.column - 1) / 2) / 3)  # CalcuLlate number of measurement points
        self.NumberofATDs = NumberofATDs

        # Seat data
        self.Seat = Seat
        self.rows_seats, self.column_seats = self.Seat.shape
        self.number_Seat = int((self.column_seats - 1) / 3)

        # plot charactristicks
        self.colors = ["red", "purple", "green", "orange","yellow"]  # Different colors for ATDs

    def Plot(self):
        """
        Generates a 3D scatter plot for ATD_1 and ATD_2.
        """
        x_data_ATD_1, y_data_ATD_1, z_data_ATD_1 = [], [], []
        x_data_ATD_2, y_data_ATD_2, z_data_ATD_2 = [], [], []

        # Collecting data for ATD_1
        for i in range(1, self.Number + 1):
            x_data_ATD_1.append(self.ATD1.iloc[0, i])
            y_data_ATD_1.append(self.ATD1.iloc[0, 71 + i])
            z_data_ATD_1.append(self.ATD1.iloc[0, 142 + i])

        # Collecting data for ATD_2
        for i in range(1, self.Number + 1):
            x_data_ATD_2.append(self.ATD1.iloc[0, 213 + i])
            y_data_ATD_2.append(self.ATD1.iloc[0, 284 + i])
            z_data_ATD_2.append(self.ATD1.iloc[0, 355 + i])

        # Creating 3D scatter plots for ATD_1 and ATD_2
        trace_ATD_1 = go.Scatter3d(
            x=x_data_ATD_1, y=y_data_ATD_1, z=z_data_ATD_1,
            mode='markers', marker=dict(color='blue', size=5), name='ATD_1'
        )

        trace_ATD_2 = go.Scatter3d(
            x=x_data_ATD_2, y=y_data_ATD_2, z=z_data_ATD_2,
            mode='markers', marker=dict(color='red', size=5), name='ATD_2'
        )

        # Create the figure and add the traces
        fig = go.Figure(data=[trace_ATD_1, trace_ATD_2])
        fig.update_layout(title="3D Scatter Plot - ATD Data", width=1000, height=600)

        # Display the plot
        fig.show()


    def Initial_condition_plot(self):
        """
        Generates a 3D scatter plot for initial conditions of ATDs and Seat.
        """
        fig = go.Figure()

        for k in range(2):
            k_offset = int(((self.column - 1) / 2)) * k  # Offset for multiple ATDs
            x_data_ATD, y_data_ATD, z_data_ATD = [], [], []
            
            # Collecting data for ATDs
            for i in range(1, self.Number + 1):
                x_data_ATD.append(self.ATD1.iloc[0, k_offset + i])
                y_data_ATD.append(self.ATD1.iloc[0, self.Number + k_offset + i])
                z_data_ATD.append(self.ATD1.iloc[0, (self.Number * 2) + k_offset + i])

            trace_ATD = go.Scatter3d(
                x=x_data_ATD, y=y_data_ATD, z=z_data_ATD,
                mode='markers', marker=dict(color=self.colors[k % len(self.colors)], size=5),
                name=f'ATD_{k + 1}'
            )
            fig.add_trace(trace_ATD)

        # Collecting data for Seat
        x_data_seat, y_data_seat, z_data_seat = [], [], []
        for i in range(1, self.number_Seat + 1):
            x_data_seat.append(self.Seat.iloc[0, i])
            y_data_seat.append(self.Seat.iloc[0, self.number_Seat + i])
            z_data_seat.append(self.Seat.iloc[0, (self.number_Seat * 2) + i])

        trace_seat = go.Scatter3d(
            x=x_data_seat, y=y_data_seat, z=z_data_seat,
            mode='markers', marker=dict(color="blue", size=5),
            name='Seat'
        )
        fig.add_trace(trace_seat)
        
        fig.update_layout(title="3D Plot - ATDs Initial Conditions")
        
        # Display the plot
        fig.show()


    @staticmethod

    def plot(x_df, y_dfs, labels=None, title="Motion Data Plot", time_limit=None):
        """
        Plots motion data (acceleration, velocity, or displacement) using Plotly.

        :param x_df: Pandas DataFrame with one column representing x-axis values (e.g., time).
        :param y_dfs: List of Pandas DataFrames with 3 columns each for y-axis values (e.g., x, y, z).
        :param labels: List of labels for each DataFrame.
        :param title: Title of the plot.
        :param time_limit: Optional time limit (tuple or integer).
        """
        # Validate input
        if not isinstance(x_df, pd.DataFrame) or x_df.shape[1] != 1:
            raise ValueError("x_df must be a DataFrame with exactly one column.")

        if not isinstance(y_dfs, list) or not all(isinstance(df, pd.DataFrame) for df in y_dfs):
            raise ValueError("y_dfs must be a list of Pandas DataFrames.")

        for df in y_dfs:
            if df.shape[1] < 1:
                raise ValueError("Each DataFrame in y_dfs must have exactly 3 columns.")

        # Get x-axis column name
        x_col = x_df.columns[0]

        # Apply time limit
        if isinstance(time_limit, tuple) and len(time_limit) == 2:
            start =time_limit[0]*10
            end = time_limit[1]*10
        elif isinstance(time_limit, int):
            start =0
            end = time_limit[1]*10
        else:
            start, end = 0, len(x_df)

        x = x_df.iloc[start:end, 0].reset_index(drop=True)
        fig = None

        for idx, y_df in enumerate(y_dfs):
            y_df = y_df.iloc[start:end]
            temp_df = pd.concat([x.reset_index(drop=True), y_df.reset_index(drop=True)], axis=1)
            temp_df.columns = [x_col] + list(y_df.columns)

            temp_fig = px.line(temp_df, x=x_col, y=temp_df.columns[1:], title=title if idx == 0 else None)

            if labels:
                temp_fig.for_each_trace(lambda t: t.update(name=f"{labels[idx]} - {t.name}"))

            if fig is None:
                fig = temp_fig
            else:
                for trace in temp_fig.data:
                    fig.add_trace(trace)

        fig.update_layout(title=title)
        fig.show()