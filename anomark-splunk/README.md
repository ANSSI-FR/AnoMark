# AnoMark for Splunk

The `anomark/` folder provides a Splunk app that you can load after compressing it as `.tar.gz` file.
You will just need these steps:
* First install splunklib from the splunk python sdk

```commandline
git clone https://github.com/splunk/splunk-sdk-python.git
cp -r splunk-sdk-python/splunklib/ ANOMARK_FOLDER/anomark-splunk/anomark/bin/
rm -r splunk-sdk-python/
```

* Create a model from your data (you can download it from Spluk in CSV format), and copy it in the `models/` folder
(or create it directly in this folder)

```commandline
python ANOMARK_FOLDER/train_from_csv.py -d DATA_PATH.csv -o ORDER(int) -c COLUMN_NAME --output ANOMARK_FOLDER/anomark-splunk/anomark/bin/models/MODEL_NAME
```

* Eventually you can create the app compressed file with the following command:

```commandline
tar -zcvf anomark.tar.gz anomark/
```

Then go into splunk main page, and click on the configuration wheel at the top of `Apps` panel. It will redirect
you to `<SPLUNK_URL>/en-GB/manager/launcher/apps/local`. There click on `Install app from file` and browse your
compressed file. Splunk will automatically intall the app with the configuration.

If you are not able to install the app through the web interface, you can copy the `anomark.tar.gz` to your
Splunk server and uncompress it in `/<SPLUNK_FOLDER>/etc/apps`.

## Use of the custom command

Once the app is installed you simply use anomark as any other command in Splunk:

```commandline
index=test_index | EventCode=4688 | anomark
```

By default `anomark` will execute on CommandLine field, with the model `bin/models/model_cmdline.dump`
(which is not provided, you have to create your own and copy it with this name). It adds a field `markov_score`
containing the log-likelihood of a `CommandLine` or of any other field you provide with a the fieldname flag :

```commandline
my_base_search | anomark fieldname=FIELD modelname=MODEL_NAME
```

The model must be located in the `<AnoMark_APP>/bin/models` folder on your Splunk Server.
