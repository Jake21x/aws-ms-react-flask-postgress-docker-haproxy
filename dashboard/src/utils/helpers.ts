export const getAsUriParameters = (data: Object) => {
  var url = "";
  for (var prop in data) {
    url +=
      encodeURIComponent(prop) + "=" + encodeURIComponent(data[prop]) + "&";
  }
  return url.substring(0, url.length - 1);
};

export const getIp = (host: string) => {
  console.log("getIp", host);
  const port = process.env.API_BASE_PORT;
  let ip = "";
  try {
    const ip_extra = host.split(":");
    ip = ip_extra[0];
  } catch (err) {
    console.log("getIp", "no report use ip");
  }
  return ip + (port === "" ? "" : `:${port}`);
};
export const getBaseEnvURL = () => {
  let ip =
    process.env.NEXT_PUBLIC_API_BASE_URL +
    "" +
    process.env.NEXT_PUBLIC_API_BASE_PORT +
    "" +
    process.env.NEXT_PUBLIC_API_BASE;
  console.log("ip", ip);
  return ip;
};
