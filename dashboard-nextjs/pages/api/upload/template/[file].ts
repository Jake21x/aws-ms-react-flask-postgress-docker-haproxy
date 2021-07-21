// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import { getIpOnly } from "@/utils/helpers";
import axios, { AxiosError } from "axios";
import { NextApiRequest, NextApiResponse } from "next";
import formidable from "formidable";
import FormData from "form-data";

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const use_ip = getIpOnly(req.headers.host);
  const baseUrl = "http://" + use_ip + req.url;
  console.log("baseUrl", req.url);
  console.log("baseUrl", baseUrl);

  const data = new formidable.IncomingForm();

  data.parse(req, (err, fields, files) => {
    console.log("api > form", { err, fields, files });

    let form = new FormData();
    form.append("file", files);

    axios
      .post(baseUrl, form, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(
        (data) => {
          console.log("data", data);
          res.status(200).json({ status: "success", message: "success" });
        },
        (err: AxiosError) => {
          res.status(503).json(err.message);
        }
      );
  });
};
