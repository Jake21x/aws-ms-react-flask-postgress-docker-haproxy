import { Flex, Text } from "@chakra-ui/layout";
import { useLocation } from "react-router";

function Page404() {
  const { pathname } = useLocation();
  return (
    <Flex justify="center" direction="column" alignItems="center">
      <Text fontWeight="bold" fontSize="lg">
        404
      </Text>
      Page not found {pathname}
    </Flex>
  );
}

export default Page404;
