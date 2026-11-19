"use client";
import { useReducer } from "react";
import { productData } from "../data/productData";
import { ProductConfig } from "../types/ProductContextType";
import { cartReducer } from "./cartReducer";
import { ProductContext } from "./productContext";
const initialState: ProductConfig[] = productData;
export default function ProductProvider({ children }: React.PropsWithChildren) {
  const [product, dispatch] = useReducer(cartReducer, initialState);
  return (
    <ProductContext.Provider value={{ product, dispatch }}>
      {children}
    </ProductContext.Provider>
  );
}
