import { useState } from "react";

interface Chat {
	id: number;
	question: string;
	answer: string;
	status: "loading" | "success" | "failed";
}

function App() {
	const [chats, setChats] = useState<Chat[]>([]);
	const [fileUrl, setFileUrl] = useState<string>("");
	const [question, setQuestion] = useState<string>("");

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		setQuestion("");

		setChats((prevChats) => [
			...prevChats,
			{
				id: prevChats.length + 1,
				question: question,
				answer: "",
				status: "loading",
			},
		]);

		try {
			// const get_api = await fetch("http://localhost:8000/");
			// const get_data = await get_api.json();
			// console.log("get_data:", get_data);
			// const response = await fetch("http://localhost:8000/api/process_pdf", {
			// 	method: "POST",
			// 	headers: {
			// 		"Content-Type": "application/json",
			// 	},
			// 	body: JSON.stringify({ fileUrl: fileUrl }),
			// });

			const response = await fetch("http://localhost:8010/api/query", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ query: question }),
			});

			const data = await response.json();
			console.log("query result:", data);

			if (data) {
				setChats((prevChats) =>
					prevChats.map((chat) =>
						chat.status === "loading"
							? {
									...chat,
									answer: data.result.answer,
									status: "success",
							  }
							: chat
					)
				);
			} else {
				setChats((prevChats) =>
					prevChats.map((chat) =>
						chat.status === "loading"
							? {
									...chat,
									answer: "Failed to get answer",
									status: "failed",
							  }
							: chat
					)
				);
			}
		} catch (error) {
			console.error("handleSubmit error:", error);
		}
	};

	return (
		<div className="bg-white h-[100vh] w-[100vw] pt-6 pb-2 overflow-hidden">
			<div className="h-full space-y-4 flex flex-col">
				<p className="text-lg font-medium text-purple-800 text-center">
					Agentic RAG
				</p>
				<div className="flex-1 overflow-hidden">
					<form
						onSubmit={handleSubmit}
						className="max-w-2xl mx-auto space-y-4 h-full flex flex-col overflow-hidden"
					>
						<div className="flex flex-col space-y-1 border-b border-b-gray-400 pb-2">
							<label htmlFor="file_path" className="text-black">
								Enter file URL
							</label>
							<input
								type="text"
								name="fileUrl"
								id=""
								className="w-full p-2 border border-gray-400 rounded shadow text-black"
								value={fileUrl}
								onChange={(e) => {
									setFileUrl(e.target.value);
								}}
							/>
						</div>
						<div className="flex-1 flex flex-col space-y-1 overflow-hidden">
							<p className="text-black font-medium">Chats</p>
							<div className="flex-1 overflow-y-auto scrollbar-thin">
								{chats &&
									chats.map((chat, index) => (
										<div
											key={index}
											className="flex flex-col space-y-2 border-b py-2"
										>
											<div className="space-y-2">
												<p className="text-black bg-gray-100 p-3">
													{chat.question}
												</p>
												<div className="p-3">
													{chat.status === "loading" ? (
														<span className="text-gray-600">Querying.....</span>
													) : chat.status === "failed" ? (
														<span className="text-gray-600">{chat.answer}</span>
													) : (
														<span className="text-gray-600">{chat.answer}</span>
													)}
												</div>
											</div>
											{/* <div className="flex items-center justify-between">
												<p className="text-black">{chat.answer}</p>
											</div> */}
										</div>
									))}
							</div>
							<div className="flex items-center space-x-2 p-3 border-t border-gray-200">
								<input
									type="text"
									name="question"
									id=""
									placeholder="Enter your question..."
									className="w-full p-2 border border-gray-400 rounded shadow text-black"
									value={question}
									onChange={(e) => {
										setQuestion(e.target.value);
									}}
								/>
								<button type="submit">Send</button>
							</div>
						</div>
					</form>
				</div>
			</div>
		</div>
	);
}

export default App;
