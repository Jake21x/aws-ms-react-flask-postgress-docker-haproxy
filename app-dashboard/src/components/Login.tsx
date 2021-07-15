import { Button } from "@chakra-ui/button";
import { Input } from "@chakra-ui/input";
import { Box, Text } from "@chakra-ui/layout";
import { useForm } from "react-hook-form";

type TLogin = {
  username: String;
  password: String;
  mode: String;
};

function Login() {
  const { register, handleSubmit, errors } = useForm<TLogin>();

  const onSubmit = (form: TLogin) => {
    console.log("onSubmit", form);
  };

  return (
    <Box>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Input name="username" ref={register({ required: true })} />
        <Input
          name="password"
          ref={register({ required: true })}
          type="password"
        />

        <Box m="1" colorScheme="red">
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
        <Button type="submit">Login</Button>
      </form>
    </Box>
  );
}

export default Login;
