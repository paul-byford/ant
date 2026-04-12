from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(name="read_doc_contents", description="Read the contents of a document")
def read_doc_contents(doc_id: str = Field(description="The ID of the document to read")):
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    return docs[doc_id]

@mcp.tool(name="edit_doc_contents", description="Edit a document by replacing a string with a new string")
def edit_doc_contents(doc_id: str = Field(description="The ID of the document to edit"), new_contents: str = Field(description="The new contents of the document"), old_contents: str = Field(description="The string to replace in the document")):
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    if old_contents not in docs[doc_id]:
        raise ValueError(f"String '{old_contents}' not found in document '{doc_id}'.")
    docs[doc_id] = docs[doc_id].replace(old_contents, new_contents)
    return f"Document '{doc_id}' updated successfully." 

@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://document/{doc_id}",
    mime_type="text/plain",
)
def get_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc

if __name__ == "__main__":
    mcp.run(transport="stdio")
