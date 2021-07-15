import { Input } from "@chakra-ui/input";
import { Box, Flex } from "@chakra-ui/layout";
import Login from "src/components/Login";

function LoginPage() {
  return (
    <Flex display="grid" h="full" placeItems="center">
      <Box w="3xl">
        <Login />
      </Box>
    </Flex>
  );
}

export default LoginPage;
