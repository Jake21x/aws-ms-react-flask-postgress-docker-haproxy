import { useDisclosure } from "@chakra-ui/hooks";
import { Flex, Text } from "@chakra-ui/layout";
import { Collapse } from "@chakra-ui/transition";
import { useEffect, useState } from "react";
import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import NotifPortal from "./components/NotifPortal";
import Page404 from "./pages/404Page";
import Dashboard from "./pages/Dashboard";
import LoginPage from "./pages/LoginPage";
import Templates from "./pages/Templates";

function App() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [networkToggle, setNetworkToggle] = useState<string | null>(null);
  const queryClient = new QueryClient();

  useEffect(() => {
    const online: any = window.addEventListener("online", () => {
      onClose();
      onOpen();
      setNetworkToggle("online");
      setTimeout(() => {
        onClose();
      }, 4000);
    });
    const offline: any = window.addEventListener("offline", () => {
      onOpen();
      setNetworkToggle("offline");
    });

    return () => {
      window.removeEventListener("online", online);
      window.removeEventListener("offline", offline);
    };
  });

  return (
    <QueryClientProvider client={queryClient}>
      <NotifPortal el="networkstatus">
        <Collapse in={isOpen} animateOpacity>
          {networkToggle === "online" ? (
            <Flex align="center" justify="center" bg="#0dc445" w="100%">
              <Text color="white" fontSize="sm" p="1">
                Your network is restored
              </Text>
            </Flex>
          ) : (
            <Flex align="center" justify="center" bg="#f51b1b" w="100%">
              <Text color="white" fontSize="sm" p="1">
                You're on offline mode
              </Text>
            </Flex>
          )}
        </Collapse>
      </NotifPortal>
      <Router>
        <Switch>
          <Route exact path="/:username/templates" component={Templates} />
          <Route exact path="/login" component={LoginPage} />
          <Route exact path="/" component={Dashboard} />
          {/* <Route exact path="/" component={Loader} /> */}
          <Route component={Page404} />
        </Switch>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
