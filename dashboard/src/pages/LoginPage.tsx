import { Box, Flex } from "@chakra-ui/layout";
import LoginFrom from "src/components/LoginFrom";

function LoginPage() {
  return (
    <Flex display="grid" h="full" placeItems="center">
      <Box w="3xl">
        <LoginFrom />
      </Box>
    </Flex>
  );
}

export default LoginPage;
