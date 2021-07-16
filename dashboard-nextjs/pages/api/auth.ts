// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import axios from "axios";
import { NextApiRequest, NextApiResponse } from "next";

export default function (req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ name: "John Doe" });

  const url = req.body.url;

  console.log("url", url);

  return { OK: "OK" };

  // axios.post(url_params).then(
  //   (res) => {
  //     console.log("res", res);
  //     setLoading(false);
  //   },
  //   (err: AxiosError) => {
  //     setLoading(false);
  //     console.log("error", err.message);
  //   }
  // );
}
