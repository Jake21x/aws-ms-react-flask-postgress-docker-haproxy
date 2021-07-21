import { Button } from "@chakra-ui/button";
import { Box, Flex, Text } from "@chakra-ui/layout";
import { Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/tabs";
import { useState } from "react";
import { Input } from "@chakra-ui/input";
import { useForm } from "react-hook-form";
import axios from "axios";
import { chain_columns } from "@/utils/columns";
import TableData from "@/components/TableData";

type FormValues = {
  file_chain: Blob;
  file_area: Blob;
  file_category: Blob;
  file_category_reference: Blob;
  file_sku: Blob;
  file_stores: Blob;
  file_stores_skus: Blob;
  file_users: Blob;
  file_users_schedules: Blob;
};

type TSheet = {
  name: String;
  column: any;
  data: any;
};

function Templates() {
  const { register, handleSubmit, errors } = useForm<FormValues>();
  const [loading, setLoading] = useState(false);

  const [Sheets, setSheet] = useState([
    {
      name: "Chain",
      column: chain_columns,
      data: [],
    },
    {
      name: "Area",
      column: chain_columns,
      data: [],
    },
    {
      name: "Agency",
      column: chain_columns,
      data: [],
    },
    {
      name: "Stores",
      column: chain_columns,
      data: [],
    },
    {
      name: "Users",
      column: chain_columns,
      data: [],
    },
    {
      name: "Users Schedules",
      column: chain_columns,
      data: [],
    },
    {
      name: "SKUs",
      column: chain_columns,
      data: [],
    },
    {
      name: "Category",
      column: chain_columns,
      data: [],
    },
    {
      name: "Category Reference",
      column: chain_columns,
      data: [],
    },
    {
      name: "Stores SKUs",
      column: chain_columns,
      data: [],
    },
  ]);

  const [active, setActive] = useState(Sheets[0]);
  const data_column: any = [];

  // const [data , setData] = useState("")

  // useEffect(()=>{

  // },[selected])

  const onSubmit = (form: any) => {
    const isactive = "file_" + active.name.toLowerCase().replaceAll(" ", "_");
    console.log("onSubmit > form", form);
    console.log("onSubmit > form", form[isactive][0]);
    uploadValue(isactive, form[isactive][0]);
  };

  const uploadValue = async (value: string, form: Blob) => {
    const newfilename = value.replace("file_", "") + ".xlsx";
    console.log("uploadValue > ", value, form);
    setLoading(true);
    var body = new FormData();
    body.append("file", form, newfilename);
    const url = "/api/upload/template/" + value.replace("file_", "");
    console.log("url", url, body);

    const result = await fetch("http://localhost:8080" + url, {
      method: "POST",
      mode: "no-cors",
      body,
    }).then((response) => console.log(response));

    // console.log("result", result);
    // result
    //   .then((responseData) => {
    //     console.log(responseData);
    //     return responseData;
    //   })
    //   .catch((error) => console.warn(error));

    // fetch(url, {
    //   method: "POST",
    //   body: bodyFormData,
    // })
    //   .then((response) => {
    //     setLoading(false);
    //     console.log("response", response);
    //   })
    //   .catch((err) => {
    //     setLoading(false);
    //     console.log("err", err);
    //   });
  };

  return (
    <Box m="3">
      <form onSubmit={handleSubmit(onSubmit)}>
        <Tabs>
          <TabList>
            {Sheets.map((value, index) => (
              <Tab
                onClick={(evt) => {
                  setActive(value);
                  evt.preventDefault();
                }}
                fontSize="sm"
                key={index}
              >
                {value.name.toUpperCase()}
              </Tab>
            ))}
          </TabList>

          <TabPanels>
            {Sheets.map((value, index) => {
              return (
                <TabPanel key={index + "" + value}>
                  <Text fontWeight="bold" my="3">
                    {value.name.toUpperCase()}
                  </Text>

                  <Flex alignItems="center">
                    <Input
                      accept=".xlsx, .xls"
                      name={
                        "file_" + value.name.toLowerCase().replace(" ", "_")
                      }
                      ref={register}
                      type="file"
                    />
                    <Button isLoading={loading} type="submit">
                      Upload
                    </Button>
                  </Flex>

                  <TableData columns={value.column} data={value.data} />
                </TabPanel>
              );
            })}
          </TabPanels>
        </Tabs>
      </form>
    </Box>
  );
}

export default Templates;
