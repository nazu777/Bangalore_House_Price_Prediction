import { useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

export default function App() {

  const [urls, setUrls] = useState("");

  const [videos, setVideos] = useState([]);

  const [quality, setQuality] =
    useState("720p");

  const analyze = async () => {

    const response =
      await axios.post(
        `${API}/analyze`,
        {
          urls: urls
            .split("\n")
            .filter(Boolean)
        }
      );

    setVideos(response.data);
  };

  const download = async () => {

    const response =
      await axios.post(
        `${API}/download`,
        {
          urls: urls
            .split("\n")
            .filter(Boolean),
          quality
        },
        {
          responseType: "blob"
        }
      );

    const blob =
      new Blob([response.data]);

    const link =
      document.createElement("a");

    link.href =
      window.URL.createObjectURL(blob);

    link.download =
      response.headers[
        "content-disposition"
      ]
        ?.split("filename=")[1]
        ?.replaceAll('"', "") ||
      "download.zip";

    link.click();
  };

  return (
    <div className="min-h-screen bg-zinc-900 text-white p-10">

      <div className="max-w-6xl mx-auto">

        <h1 className="text-5xl font-bold mb-10">
          YT Downloader
        </h1>

        <textarea
          className="
          w-full
          h-52
          p-5
          rounded-2xl
          text-black
          text-lg
          "
          placeholder="
One URL per line
or playlist URL
"
          value={urls}
          onChange={(e) =>
            setUrls(e.target.value)
          }
        />

        <button
          onClick={analyze}
          className="
          mt-6
          px-8
          py-4
          bg-blue-600
          rounded-2xl
          text-lg
          "
        >
          Analyze
        </button>

        <div className="mt-10 space-y-8">

          {videos.map((v, i) => (

            <div
              key={i}
              className="
              bg-zinc-800
              p-6
              rounded-2xl
              "
            >

              <h2 className="text-2xl font-bold">
                {v.title}
              </h2>

              {v.thumbnail && (

                <img
                  src={v.thumbnail}
                  className="
                  w-[450px]
                  rounded-2xl
                  mt-5
                  "
                />

              )}

              <div className="
              flex
              gap-3
              flex-wrap
              mt-5
              ">

                {v.qualities?.map((q) => (

                  <button
                    key={q}
                    onClick={() =>
                      setQuality(q)
                    }
                    className={`
                    px-5
                    py-3
                    rounded-xl
                    ${
                      quality === q
                        ? "bg-green-600"
                        : "bg-zinc-700"
                    }
                    `}
                  >
                    {q}
                  </button>

                ))}

              </div>

            </div>

          ))}

        </div>

        <button
          onClick={download}
          className="
          mt-10
          px-10
          py-5
          bg-green-600
          rounded-2xl
          text-xl
          "
        >
          Download
        </button>

      </div>

    </div>
  );
}