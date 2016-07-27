[Synopis]
For effective verify the software quality without too many manul control.
This is for trigger multiple platforms and automatically return the result report by email. I only post some scripts which I used for this project.

</br>[Installation]
</br>pyspherie
</br>html

</br>[Files]
</br>trigger.py 
</br> - the main control follow
</br>config.py 
</br> - copy source to worker machines
</br> - worker info: account, pwd
</br>postman.py
</br> - send mail and attachments
</br>virtualmachine.py
</br> - control Esxi and workers
</br>report.py
</br> - generate report
</br>time_consumptioon.py
</br> - calculate test cases cost 
</br>watchdog.py
</br> -monitor the main follows
