import { Button } from "@chakra-ui/button";
import { Box } from "@chakra-ui/layout";
import { useDropzone } from "react-dropzone";

function Uploads() {
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,
  } = useDropzone({ accept: "application/vnd.ms-excel" });

  const getColor = (props: any) => {
    if (props.isDragAccept) {
      return "#00e676";
    }
    if (props.isDragReject) {
      return "#ff1744";
    }
    if (props.isDragActive) {
      return "#2196f3";
    }
    return "#eeeeee";
  };

  return (
    <Box m="3">
      <form>
        <Box
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            padding: "20px",
            borderWidth: "2px",
            borderRadius: "2px",
            borderColor: "#eeeeee",
            borderStyle: "dashed",
            backgroundColor: "#fafafa",
            color: "#bdbdbd",
            outline: "none",
            transition: "border .24s ease-in-out",
          }}
          {...getRootProps({ isDragActive, isDragAccept, isDragReject })}
        >
          <input {...getInputProps()} />
          <p>Drag 'n' drop some files here, or click to select files</p>
        </Box>

        <Button mt="1">Upload</Button>
      </form>
    </Box>
  );
}

export default Uploads;
