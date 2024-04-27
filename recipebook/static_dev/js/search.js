const inp_name = document.getElementById("search-name");
const inp_category = document.getElementById("search-category");
const inp_kitchen = document.getElementById("search-kitchen");
const inp_level = document.getElementById("search-level");

const btn_sort_name = document.getElementById("sort-name");
const btn_sort_new = document.getElementById("sort-new");
const btn_sort_easy = document.getElementById("sort-easy");
const btn_sort_fast = document.getElementById("sort-fast");

const btn = document.getElementById("search-btn");
const clear_btn = document.getElementById("search-clear-btn");

const ingredient_container = document.getElementById("search-ingredient-container");
const ingredient_include = document.getElementById("search-ingredient-include");
const ingredient_exclude = document.getElementById("search-ingredient-exclude");
const ingredient_input = document.getElementById("search-ingredient-input");
const ingredient_list = document.getElementById("search-ingredient-list");

const pagination = document.getElementById("pagination");

ingredient_input.addEventListener("focus", () => ingredient_list.classList.add("search_visible"))
window.addEventListener("click", e =>
{
	let el = e.target;
	let found = false;
	while (el)
	{
		if (el == ingredient_container)
		{
			found = true;
			break
		}
		el = el.parentElement
	}
	if (!found)
		ingredient_list.classList.remove("search_visible");
})
window.addEventListener("keyup", e =>
{
	if (e.key == "Escape")
		ingredient_list.classList.remove("search_visible");
})
ingredient_input.addEventListener("input", () =>
{
	ingredient_list.classList.add("search_visible");
	const search = ingredient_input.value.trim().toLowerCase().replaceAll(/\s+/g, " ");
	let found = false;
	for (let i = 0; i < ingredient_list.children.length - 1; i++)
	{
		const el = ingredient_list.children[i];
		if (el.children[0].innerText.toLowerCase().includes(search))
		{
			el.style.display = "";
			found = true;
		}
		else
			el.style.display = "none";
	}
	const not_found_el = ingredient_list.children[ingredient_list.children.length - 1];
	not_found_el.style.display = found ? "none" : "";
})

const url = new URL(window.location);
inp_name.value = url.searchParams.get("sn") || "";
inp_category.value = url.searchParams.get("sc") || "";
inp_kitchen.value = url.searchParams.get("sk") || "";
inp_level.value = url.searchParams.get("sl") || "";

const ingredients_include = url.searchParams.get("si")?.split("-").filter(v => v && !isNaN(+v)) || [];
const ingredients_exclude = url.searchParams.get("sie")?.split("-").filter(v => v && !isNaN(+v)) || [];


for (let i = 0; i < ingredient_list.children.length - 1; i++)
{
	const el = ingredient_list.children[i];
	const id = el.getAttribute("data-id");
	const name = el.children[0].innerText
	const cbx_include = el.querySelector("#search-ingredient-include-chb")
	const cbx_exclude = el.querySelector("#search-ingredient-exclude-chb")
	const include_i = ingredients_include.indexOf(id);
	const exclude_i = ingredients_exclude.indexOf(id);
	if (include_i >= 0)
	{
		ingredients_include[include_i] = { id, name };
		cbx_include.checked = true;
	}
	if (exclude_i >= 0)
	{
		ingredients_exclude[exclude_i] = { id, name };
		cbx_exclude.checked = true;
	}
	cbx_include.addEventListener("change", () =>
	{
		const i = ingredients_include.findIndex(v => v.id == id);
		if (cbx_include.checked)
		{
			if (i < 0) ingredients_include.push({ id, name });

			cbx_exclude.checked = false;
			const i2 = ingredients_exclude.findIndex(v => v.id == id);
			if (i2 >= 0) ingredients_exclude.splice(i2, 1);
		}
		else
		{
			ingredients_include.splice(i, 1);
		}
		displayAllIngredients();
	});
	cbx_exclude.addEventListener("change", () =>
	{
		const i = ingredients_exclude.findIndex(v => v.id == id);
		if (cbx_exclude.checked)
		{
			if (i < 0) ingredients_exclude.push({ id, name });

			cbx_include.checked = false;
			const i2 = ingredients_include.findIndex(v => v.id == id);
			if (i2 >= 0) ingredients_include.splice(i2, 1);
		}
		else
		{
			ingredients_exclude.splice(i, 1);
		}
		displayAllIngredients();
	});
}

function displayIngredients(container, ingredients)
{
	container.innerHTML = "";
	for (const ingredient of ingredients)
	{
		const el = document.createElement("span");
		el.innerText = ingredient.name;
		container.appendChild(el);
	}
}
function displayAllIngredients()
{
	displayIngredients(ingredient_include, ingredients_include);
	displayIngredients(ingredient_exclude, ingredients_exclude);
}
displayAllIngredients()

pagination.querySelectorAll("button")
	.forEach(el => el.addEventListener("click", () =>
	{
		const url = new URL(window.location);
		url.searchParams.set("page", el.getAttribute("data-page"));
		window.location = url;
	})
);

clear_btn.addEventListener("click", () =>
{
	const url = new URL(window.location);
	window.location = url.pathname;
})


btn.addEventListener("click", search);
inp_name.addEventListener("keypress", e =>
{
	if (e.key == "Enter") search();
})

function search()
{
	const url = new URL(window.location);
	url.searchParams.set("page", 1);
	url.searchParams.set("sn", inp_name.value);
	url.searchParams.set("sc", inp_category.value);
	url.searchParams.set("sk", inp_kitchen.value);
	url.searchParams.set("sl", inp_level.value);
	url.searchParams.set("si", ingredients_include.map(v => v.id).join("-"));
	url.searchParams.set("sie", ingredients_exclude.map(v => v.id).join("-"));
	window.location = url;
}

function sort(type)
{
	const url = new URL(window.location);
	url.searchParams.set("page", 1);
	url.searchParams.set("order", type);
	window.location = url;
}

btn_sort_name.addEventListener("click", () => sort("name"));
btn_sort_new.addEventListener("click", () => sort("new"));
btn_sort_easy.addEventListener("click", () => sort("easy"));
btn_sort_fast.addEventListener("click", () => sort("fast"));
