"use client";
import { useReducer } from "react";
import { productData } from "../data/productData";
import { ProductConfig, ShopState } from "../types/ProductContextType";
import { cartReducer } from "./cartReducer";
import { ProductContext } from "./productContext";
const initialState: ShopState = {
  product: productData,
  cartProdcuts: [],
};
export default function ProductProvider({ children }: React.PropsWithChildren) {
  const [shop, dispatch] = useReducer(cartReducer, initialState);
  return (
    <ProductContext.Provider value={{ shop, dispatch }}>
      {children}
    </ProductContext.Provider>
  );
}
