import { useState } from "react";
import axios from "axios";

const Textarea = () => {
    const [input, setInput] = useState("");
    const [output, setOutput] = useState("");
    const client = axios.create({
        baseURL: "http://127.0.0.1:8000/",
    });

    const summarize = () => {
        client
            .post("/textsum/", { text: input })
            .then((res) => setOutput(res.data[0]["summary_text"]));
    };

    return (
        <>
            <div className="mainTextArea mx-20 my-8 w-[53%]">
                <div className="intext flex">
                    <h1 className="font-modern text-gray-300 font-semibold text-2xl mx-6">
                        In:{" "}
                    </h1>
                    <textarea
                        className=" ring-2 text-gray-600 ring-gray-400 rounded-md font-modern p-1"
                        id=""
                        cols={100}
                        rows={15}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                    ></textarea>
                </div>
                <div className="outtext flex mt-5">
                    <h1 className="font-modern text-gray-300 font-semibold text-2xl mx-3">
                        Out:{" "}
                    </h1>
                    <textarea
                        className="text-gray-600 ring-2 ring-[#54D0AB] rounded-md font-modern p-1"
                        id=""
                        cols={100}
                        rows={8}
                        value={output}
                        onChange={(e) => setOutput(e.target.value)}
                    ></textarea>
                </div>
                <div className="w-full flex justify-center">
                    <button
                        className=" ml-16 bg-red-300 text-white w-[20%] h-10 font-modern font-semibold rounded-lg drop-shadow-md transition-all mt-10 hover:drop-shadow-xl hover:translate-y-1"
                        onClick={summarize}
                    >
                        Summarize
                    </button>
                </div>
            </div>
        </>
    );
};

export default Textarea;
