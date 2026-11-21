"use client";
/*import { useProduct } from "./hooks/useProduct";
import { productData } from "./data/productData";
import { useState } from "react";
import Button from "./Button";
import { ProductConfig } from "./types/ProductContextType";
export default function ShopScreen() {
  const { dispatch } = useProduct();
  const [selectProduct, setSelectProduct] = useState<ProductConfig>({
    id: 0,
    title: "",
  });
  const handleProduct = (selectedProduct: ProductConfig) => {
    setSelectProduct((prev) => ({ ...prev, selectedProduct }));
    console.log("User Product: ", selectedProduct);
  };
  return (
    <div>
      {productData.map((product) => (
        <div key={product.id}>
          <h3>{product.title}</h3>
          <Button
            onClick={() => {
              handleProduct(product);
              dispatch({ type: "ADD_TO_CART", payload: selectProduct });
            }}
          >
            Add To Cart
          </Button>
        </div>
      ))}
    </div>
  );
}*/

import { useProduct } from "./hooks/useProduct";
import { productData } from "./data/productData";
import Button from "./Button";

export default function ShopScreen() {
  const { dispatch } = useProduct();

  return (
    <section className="mx-auto min-h-[70vh] max-w-7xl px-6 py-12">
      {/* Heading */}
      <div className="mb-10">
        <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-green-700">
          AURA Retail Store
        </p>

        <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Explore Products
        </h1>

        <p className="mt-3 max-w-xl text-sm leading-6 text-gray-500">
          Browse available grocery items and add your selections to the cart.
        </p>
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {productData.map((product) => (
          <div
            key={product.id}
            className="group flex flex-col rounded-2xl border border-gray-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:border-green-200 hover:shadow-lg"
          >
            {/* Product Image Placeholder */}
            <div className="mb-5 flex aspect-square items-center justify-center rounded-xl bg-green-50 transition-colors duration-200 group-hover:bg-green-100">
              <span className="text-5xl text-green-700 transition-transform duration-200 group-hover:scale-110">
                🛒
              </span>
            </div>

            {/* Product Details */}
            <div className="flex flex-1 flex-col">
              <h3 className="text-lg font-semibold text-gray-900 transition-colors duration-200 group-hover:text-green-800">
                {product.title}
              </h3>

              <div className="mt-auto pt-5">
                <Button
                  className="w-full rounded-lg bg-green-800 px-4 py-3 text-sm font-semibold text-white transition duration-200 hover:bg-green-900 hover:shadow-md active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-600 focus-visible:ring-offset-2 cursor-pointer"
                  onClick={() =>
                    dispatch({
                      type: "ADD_TO_CART",
                      payload: product,
                    })
                  }
                >
                  Add to Cart
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
