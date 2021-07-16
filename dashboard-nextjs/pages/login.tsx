import { Input } from "@chakra-ui/input";
import { Box, Flex } from "@chakra-ui/layout";
import LoginFrom from "../components/LoginFrom";

function Login() {
  return (
    <Flex display="grid" h="full" placeItems="center">
      <Box w="3xl">
        <LoginFrom />
      </Box>
    </Flex>
  );
}

export default Login;
