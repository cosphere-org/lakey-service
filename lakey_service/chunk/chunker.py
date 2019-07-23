import numpy as np

def chunker_algorithm(ci, cube_size):

    table = ci.costam
    chunks_borders_alg = split(table)

    def split(table):
        split_axis = find_split_axis(table)
        element_count = table[split_axis].count()

        median = np.median(table[split_axis])
        split_table1 = table[table[split_axis] > median]
        split_table2 = table[table[split_axis] < median]

        table_median = table.loc[table[split_axis] == median]
        half_of_all = table[split_axis].count()/2

        if split_table1[split_axis].count() != split_table2[split_axis].count():
            split_table1 = split_table1.append(
                table_median.head(int(half_of_all - split_table1[split_axis].count())))
            split_table2 = split_table2.append(
                table_median.tail(int(half_of_all - split_table2[split_axis].count())))

        if element_count > cube_size:
            return split(split_table1) + split(split_table2)
            
        else:
            chunk = {}
            for col in table.columns:
                chunk["column"] = col
                chunk["minimum"] = table.col.min()
                chunk["maximun"] = table.col.max()

            return [chunk]

    def find_split_axis(table):
        greatest_variance = 0
        for col in table.columns:
            variance = table[col].var()
            if variance > greatest_variance:
                greatest_variance = variance
                split_axis = col
        return split_axis


    return chunks_borders_alg


chunks_borders = chunker_algorithm(ci, 10000)

chunks = []
for border in chunks_borders:
    chunks.append(Chunk(
        catalogue_item=ci,
        borders=border))

Chunk.objects.bulk_create(chunks)