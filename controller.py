from tkinter import messagebox

class CaptionController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_filename = None
        self.load_next()

    def load_next(self):
        next_data = self.model.get_next()
        if next_data is None:
            messagebox.showinfo("Fine", "Hai completato tutte le immagini!")
            self.view.root.quit()
            return
        filename, image_path, caption = next_data
        self.current_filename = filename
        stats = self.model.get_stats()
        self.view.display_image_and_caption(image_path, caption, stats)

    def submit_caption(self, caption):
        # Controlla se la caption è già presente (case insensitive)
        duplicate = (self.model.df_output['caption'].str.lower() == caption.lower()).any()

        if duplicate:
            # Mostra finestra con scelta
            result = messagebox.askyesno(
                "Attenzione",
                "Questa caption è già presente. Vuoi salvarla lo stesso?\n\n"
                "Premi 'Sì' per ignorare l'avviso e salvare.\n"
                "Premi 'No' per tornare indietro e modificare."
            )
            if not result:
                # L'utente ha scelto di non salvare adesso, torna alla GUI senza avanzare
                return

        # Se qui, o non c'erano duplicati o utente ha deciso di ignorarli
        self.model.save_caption(self.current_filename, caption, skipped=False)
        self.load_next()

    def skip_caption(self):
        self.model.save_caption(self.current_filename, "", skipped=True)
        self.load_next()
