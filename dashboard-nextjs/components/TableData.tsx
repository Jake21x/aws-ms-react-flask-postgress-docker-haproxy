import DataTable from "react-data-table-component";

interface props {
  data: any;
  columns: any;
}

function TableData({ columns, data }: props) {
  return <DataTable noTableHead columns={columns} data={data} />;
}

export default TableData;
