class Chunk:
    def __init__(self, global_df):
        self.global_df = global_df
        self.max_count = 0
        self.borders = []

    def division(self, local_df=None):
        local_df = local_df if local_df is not None else self.global_df
        col_to_slice = local_df.var().idxmax()
        local_df = local_df.sort_values(col_to_slice)
        count = local_df.index.size
        median = int(count / 2)

        if not count <= self.max_count:
            left_half_df = local_df.iloc[:median]
            self.division(left_half_df)

            right_half_df = local_df.iloc[median:]
            self.division(right_half_df)
        else:
            border = []
            for col_name in local_df:
                col = local_df[col_name]
                border.append([col.min(), col.max(), count, col_name])
            self.borders.append(border)
            return

    def clear_borders(self):
        self.borders.clear()

    def set_max_count(self, max_count):
        self.max_count = max_count