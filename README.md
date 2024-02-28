# VISUAL ASSISTANT

**HOW TO USE:**

**Il visual assistant ti permette di controllare alcune funzioni del S.O. e/o del browser attraverso l’utilizzo di gesture della mano.**

**Tra una gesture e un’altra aspettare la notifica di ready per utilizzare una nuova gesture.**

**GESTURE DISPONIBILI:**

1. **Scroll Up**

1. **Scroll Down**

1. **Minimize**

1. **Volume Control**

1. **Next Page**

1. **Previous Page**

**Scrolling**

È possibile effettuare lo scroll della pagina web utilizzando la mano rivolta con il palmo verso la camera effettuando il gesto di scroll up o di scroll down.

Tieni la posizione della mano e delle dita finchè non viene eseguito lo scrolling, una volta attivato è possibile passare da scroll up a scroll down semplicemente passando da un gesto a un altro senza dover aspettare l’attivazione della gesture:

**SCROLL UP: mantieni l’indice e il medio rivolti verso L’ALTO in questo modo**

![image](./Docs/Aspose.Words.8e04d17c-b897-4faf-a164-16dc6635a86b.001.png)

**SCROLL DOWN: mantieni l’indice e il medio rivolti verso IL BASSO in questo modo**

![image](./Docs/Aspose.Words.8e04d17c-b897-4faf-a164-16dc6635a86b.002.png)

Per terminare la lettura della gesture, tenere la mano fuori dalla vista della camera, una notifica ti dirà quuando la lettura è terminata

**Minimize**

È possibile minimizzare la finestra aperta in primo piano in quel momento sul display utilizzando il pungo chiuso con palmo rivolto verso la camera in questo modo:

![image](./Docs/Aspose.Words.8e04d17c-b897-4faf-a164-16dc6635a86b.003.png)

**Volume Control**

È possibile attivare il volume control effettuando il seguente gesto, tieni il gesto finchè non viene attivata la gesture.

![image](./Docs/Aspose.Words.8e04d17c-b897-4faf-a164-16dc6635a86b.004.png)

Congiungi indice e pollice nel seguente modo per abbassare gradualmente il volume, e mantieni la posizione finchè non raggiunto il livello del volume desiderato, dopodichè tieni la mano fuori dalla vista della camera per terminare la lettura.

![image](./Docs/Aspose.Words.8e04d17c-b897-4faf-a164-16dc6635a86b.005.png)

Tieni indice e pollice alla distanza massima per aumentare gradualmente il volume, portare la mano fuori l’inquadratura per terminare la lettura.

![image](./Docs/Aspose.Words.8e04d17c-b897-4faf-a164-16dc6635a86b.006.png)

Una notifica ti dirà quando la lettura è terminata.

**Change Page**

È possiblie cambiare pagina del browser.

**PREVIOUS PAGE: Mantieni l’indice e il medio rivolti verso la tua SINISTRA in questo modo per tornare alla pagina precedentemente visitata.**

![image](./Docs/Aspose.Words.8e04d17c-b897-4faf-a164-16dc6635a86b.007.png)

**NEXT PAGE: Mantieni l’indice e il medio rivolti verso la tua DESTRA in questo modo per andare alla pagina successiva.**

![image](./Docs/Aspose.Words.8e04d17c-b897-4faf-a164-16dc6635a86b.008.png)

**Realizzazione:**

L’applicazione funziona grazie all’utilizzo di una rete neurale addestrata nel riconoscere le varie gesture con l’integrazione della libreria “MediaPipe” che permette di estrarre le informazioni posizionali della mano e delle dita grazie a dei landmarks.

DATASET:

Il dataset raccoglie 360 frame per ogni singola gesture, ogni frame contiene 21 landmarks caratterizzati dalle posizioni spaziali x,y e la distanza dalla camera z.

![image](./Docs/Aspose.Words.8e04d17c-b897-4faf-a164-16dc6635a86b.009.png)

La classe **handDetector()** contiene le funzioni **findHands()** e **findPosition(),** la prima ha il compito di rilevare tutti i landmarks grazie al metodo **.process()** ( di mediapipe), su un singolo frame, e di disegnarli, mentre la **findPosition()** prende i landmarks e li inserisce in una lista che viene quindi riempita con le posizioni spaziali se la mano viene rilevata, o una lista di ‘0’ se non vi è alcuna mano.

```
class handDetector():
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    # It searches for hands in the frame, and produces landmarks that trace their movement
    def findHands(self, frame, draw=True):

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        # Processes the hands and returns the landmarks
        self.results = self.hands.process(imgRGB)

        imgRGB.flags.writeable = True
        # in results the multi_hand_landmarks field contains the ID and
        # position of the landmarks found by the hands.process function
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw the landmarks
                    self.mpDraw.draw_landmarks(frame, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return frame

    # Saves the spatial positions of the landmarks and returns a list that
    # associates the positions of the landmarks over time with each id
    def findPosition(self, frame, handNo=0, draw=False):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):

                h, w, c = frame.shape
                cx, cy, cz = int(lm.x \* w), int(lm.y \* h), lm.z
                test = np.array([cx, cy, cz]).flatten()
                lmList.extend(test)
        else:
            lmList = (np.zeros(21\*3)) #if there aren't data to collect fill the list with a 0 matrix

        return lmList
```

Il dataset è stato raccolto è contestualmente sono state applicate le etichette corrispondenti, una per ogni gesture.

```
class Labeler:
    def __init__(self):
        label_map = {}
        working_sequences, labels = [], []
        DATA_PATH = os.path.join('MP_data')
        list_actions = os.listdir(DATA_PATH)
        for action in list_actions:
            dirPath = os.path.join(DATA_PATH, action, )
            print(action)
            # add action to label_map if it didn't exist beforehand
            label_map.setdefault(action, len(label_map.values()))
            sequences = get_sequences(dirPath)

            for sequence in sequences:
                window = []
                for frame in os.listdir(os.path.join(dirPath, sequence)):
                    file = os.path.join(dirPath, sequence, frame)
                    if os.path.isfile(file):
                        res = np.load(file)
                        window.append(res)
                if len(window) > 0:
                    working_sequences.append(window)
                    labels.append(label_map[action])
        print(labels)
        x = np.asarray(working_sequences)
        y = to_categorical(labels).astype(int)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.05, shuffle=True,random_state=50)
        pass
    pass
```

#### Rete Neurale:

È stata utilizzata l’api Keras di Tensorflow per la costruzione della rete neurale attua al riconoscimento delle gesture.

È stato utilizzato un modello di tipo sequenziale, in cui i livelli vengono aggiunti uno dopo l’altro in sequenza. Questo tipo di modello è particolarmente utile per la creazione di reti neurali feedforward, dove i dati fluiscono direttamente attraverso la rete da uno strato all’altro senza cicli o connessioni complesse.

```
model = Sequential()
# 30 is the frame's number, 63 is the number of values, 3 for each hand landmark 21 * (x, y , z)
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(1, 63)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
# the last layer gives us an array of probability whose sum is 1
model.add(Dense(actions.shape[0], activation='softmax'))

# Model Compile
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
# init labeler
labeler = lb.Labeler()
model.fit(labeler.X_train, labeler.y_train, epochs=2000, callbacks=[tb_callback], validation_split=0.25,batch_size=20)
```

L’addestramento è stato eseguito in 2000 epochs, come funzione di attivazione dei layer è stata usata una ReLu (Rectified Linear Unit) che restituisce x se x è positivo 0 altrimenti restituisce 0, particolarmente usata per compiti di visione artificiale per la sua efficienza computazionale.

Riconoscimento:

Inizialmente viene caricato il modello precedentemente addestrato e salvato, in seguito viene aperto un canale video con lo scopo di acquisire nuovi landmarks in tempo reale, che verranno poi classificati con il modello per riconoscere la gesture.

```
def take_command(folder: str = "./../TrainedModel.h5", model=None):
    if model is None:
        model = load_model(folder)
    # Detection vaiables
    sequence = []
    sentence = []
    predictions = deque()
    threshold = 0.6
    # init the camera
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    detector = ht.handDetector(detectionCon=0.75)
    while True:
        # get the current frame
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)
        # print(np.shape(lmList))
        sequence = [lmList]
        # if len(sequence) == 30:
        res = model.predict(np.expand_dims(sequence, axis=0))[0]
        frame = prob_viz(res, actions, frame, colors)
        print(res)
        if np.max(res) >= threshold and actions[np.argmax(res)] != "Nothing":
            predictions.append(actions[np.argmax(res)])
            # # Viz probabilities # we only visualize if there is an action with more probability than the threshold
            # #after #x frames of predictions it checks if there is one which occupied more than 80% frames
            if len(predictions) > frame_threshold:
                counter = Counter(predictions)
                predictions.clear()
                most = counter.most_common(1)[0]
                # # most = (name , #of occurrences)
                if most[1] >= frame_threshold \* 0.8:
                    # #predicted action:
                    cap.release()
                    cv2.destroyAllWindows()
                    return most[0], model
                    pass
            pass
        pass
        cv2.imshow("Frame", frame)
        # # added functionality to close when pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return None, model
```

la predict del modello ci restituisce un array di probabilità di appartenenza a una delle classi del modello, in base alla quale viene operata la scelta della gesture di eseguire tramite il metodo **takeQueries()**

```
def take_queries():
    volume_manager = VolumeManager(0)
    kpm = KeyPressManager()
    model = load_model("./TrainedModel.h5")
    while True:
        #speak("checking for new command")
        Hello()
        query, \_ = take_command("./TrainedModel.h5", model)
        if query is not None:
            query = query.lower()
        if query == "minimize":
            n.notify(n.enumNotifications.Minimize)
            minimizeOpenWindow()
            pass
        elif query == "scrollup" or query == "scrolldown":
            n.notify(n.enumNotifications.ScrollS)
            scroll(model)
            n.notify(n.enumNotifications.ScrollF)
            pass
        elif query == "next":
            n.notify(n.enumNotifications.Next)
            kpm.nextPage()
            pass
        elif query == "previous":
            n.notify(n.enumNotifications.Previous)
            kpm.lastPage()
            pass
        elif query == "volume":
            n.notify(n.enumNotifications.VolumeS)
            volume_manager.captureChangeVolume()
            n.notify(n.enumNotifications.VolumeF)
            pass
        elif query == "exit" or query is None:
            break
            pass
        pass
    pass
```
