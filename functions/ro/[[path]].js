/* Romanian. See ../_lang.js - every language answers the same way. */
import { serve } from "../_lang.js";

export const onRequest = (context) => serve(context, "ro");
