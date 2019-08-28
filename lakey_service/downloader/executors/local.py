import pandas
import numpy

numpy_type_to_column_type = {
    'int64': 'INTEGER',
}


def normalize_hist(hist, col_type):
    from catalogue.models import CatalogueItem
    python_type = CatalogueItem.column_type_to_python_type[
        numpy_type_to_column_type[col_type]
    ]
    return [
        {
            'value_min': python_type(hist[1][hist_idx]),
            'value_max': python_type(hist[1][hist_idx + 1]),
            'count': python_type(hist[0][hist_idx])
        } for hist_idx in range(len(hist[0]))
    ]


class LocalExecutor:

    glob_df = None

    def get_df(self, c_i):
        if self.glob_df is None:
            self.glob_df = pandas.read_csv(c_i.data_path)
        return self.glob_df

    def get_spec(self, c_i):
        df = self.get_df(c_i)
        spec = []

        for col_name in df:
            spec.append({
                'name': col_name,
                'size': self.get_size(col_name, c_i),
                'type': numpy_type_to_column_type[df.dtypes[col_name].name],
                'is_enum': False,
                'is_nullable': False,
                'distribution': self.get_distribution(col_name, c_i)
            })

        return spec

    def get_sample(self, c_i):
        pass

    def get_size(self, col_name, c_i):
        df = self.get_df(c_i)
        size = df[col_name].memory_usage()
        return size

    def get_distribution(self, col_name, c_i):
        df = self.get_df(c_i)
        hist = numpy.histogram(df[col_name])
        norm_hist = normalize_hist(hist, df[col_name].dtype.name)
        return norm_hist




