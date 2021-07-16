import { Button } from "@chakra-ui/button";
import { Input } from "@chakra-ui/input";
import { Box, Text } from "@chakra-ui/layout";
import axios, { AxiosError } from "axios";
import { useState } from "react";
import { useForm } from "react-hook-form";

type TLogin = {
  username: String;
  password: String;
  mode: String;
  appversion: String;
  device_info: String;
  device_id: String;
};

function LoginFrom() {
  const { register, handleSubmit, errors } = useForm<TLogin>();
  const [loading, setLoading] = useState(false);

  const onSubmit = (form: TLogin) => {
    // http://34.221.170.139:8080
    const url_params = `/api/gmsi/mobiletracker/login_api?username=${form.username}&password=${form.password}&device_id=${form.device_id}&appversion=${form.appversion}&device_info=${form.device_info}`;
    console.log("url_params", url_params);
    setLoading(true);
    axios.post(url_params).then(
      (res) => {
        console.log("res", res);
        setLoading(false);
      },
      (err: AxiosError) => {
        setLoading(false);
        console.log("error", err.message);
      }
    );
    console.log("onSubmit", form);
  };

  return (
    <Box>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Input
          name="username"
          defaultValue="DP-AC1"
          ref={register({ required: true })}
        />
        <Input
          name="password"
          defaultValue="MNC2021"
          ref={register({ required: true })}
          type="password"
        />
        <Input
          name="appversion"
          defaultValue="v03032020"
          ref={register({ required: true })}
        />
        <Input
          name="device_id"
          defaultValue="d81edde9172f-caba8fde38179625234"
          ref={register({ required: true })}
        />
        <Input
          name="device_info"
          defaultValue="OPPO-CPH1909"
          ref={register({ required: true })}
        />

        <Box m="1">
          {errors.username && (
            <Text fontSize="xs" textAlign="start" color="tomato">
              username is required!
            </Text>
          )}
          {errors.password && (
            <Text fontSize="xs" textAlign="start" color="tomato">
              password is required!
            </Text>
          )}
        </Box>
        <Button isLoading={loading} type="submit">
          Login
        </Button>
      </form>
    </Box>
  );
}

export default LoginFrom;
