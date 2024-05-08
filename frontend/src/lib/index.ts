// place files you want to import through the `$lib` alias in this folder.

let filesRoot = import.meta.env.VITE_FILE_SERVER ?? "http://localhost:3000/";

export { filesRoot };
