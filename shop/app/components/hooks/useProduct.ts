"use client";
import { useContext } from "react";
import { ProductContext } from "../context/productContext";

export function useProduct() {
  const context = useContext(ProductContext);
  if (!context) throw new Error("Provider Must be wrapped");
  return context;
}
