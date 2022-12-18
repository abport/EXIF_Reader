#*******************************************************
# R script nMonte.R
# Find mixture composition which minimizes
# the averaged genetic distance to target.
# Penalizing of distant admixtures.
# Activate with: source('nMonte3_temp.R')
# Use: getMonte(datafile, targetfile)
# both files should be comma-separated csv.
# Utilities:
# subset_data(): Collecting rows from datasheet
# aggr_pops(): Average populations
# tab2comma(): tab-separated to comma-separated
# last modified: headStrings 
# v10.4 Huijbregts 8 jan 2018
#*******************************************************

# default global constants
batch_def  =  500   # default rows of sample randomly drawn from data file
cycles_def = 1000   # default number of cycles
pen_def    = 0.001  # default penalty

# START OF GETMONTE FUNCTION
getMonte <- function(datafile,targetfile,
            omit='',Nbatch=batch_def,Ncycles=cycles_def,save=F,pen=pen_def) {

    # define AlGORITHM embedded function
    do_algorithm <- function(selection, targ) {
        mySel <- as.matrix(selection, rownames.force = NA)       
        myTg <- as.matrix(targ, rownames.force = NA)
        dif2targ <- sweep(mySel, 2, myTg, '-')    # data - target       
        Ndata <- nrow(dif2targ)
        kcol <- ncol(dif2targ)
        rowLabels <- rownames(dif2targ)
        # preallocate data
        matPop    <- matrix(NA_integer_,  Nbatch, 1, byrow=T)
        dumPop    <- matrix(NA_integer_,  Nbatch, 1, byrow=T) 
        matAdmix  <- matrix(NA_real_, Nbatch, kcol, byrow=T)
        dumAdmix  <- matrix(NA_real_, Nbatch, kcol, byrow=T)
        matPop    <- sample(1:Ndata,Nbatch,replace=T)        
        # fill matPop with random row numbers 1:Ndata from datafile
        matAdmix   <- dif2targ[matPop,]
        # iniatialize objective function         
        colM1 <- colMeans(matAdmix)
        eval1 <- (1+pen) * sum(colM1^2)  
        # Ncycles iterations
        for (c in 1:Ncycles) {
            # fill batch data
            dumPop <- sample(1:Ndata, Nbatch, replace=T)
            dumAdmix   <- dif2targ[dumPop,]
            # loop thru batch
            # penalty is squared distance of sample to target
            # objective function = 
            #     squared dist of batch mean to target + coef*penalty
            # minimize objective function 
            for (b in 1:Nbatch) {
                # test alternative pop
                store <- matAdmix[b,]
                matAdmix[b,] <- dumAdmix[b,]
                colM2 <- colMeans(matAdmix)
                eval2 <- sum(colM2^2) + pen*sum(matAdmix[b, ]^2)
                # conditional adjust
                if (eval2 <= eval1) {
                    matPop[b] <- dumPop[b]
                    colM1 <- colM2
                    eval1 <- eval2
                } else {matAdmix[b,] <- store}
            } # end batch
        } # end cycles
        # Collect output
        # get fit of target
        fitted <- t(colMeans(matAdmix) + myTg[1,])
        # collect sampled populations
        # split labels of reference samples
        popl <- headStrings(rowLabels[matPop], mySep=':')
        populations <- factor(popl)
        # return list of 2 objects
        return(list('estimated'=fitted, 'pops'=populations))
    }   # end do_algorithm    
    
    # define OUTPUT embedded function
    # except pop correlations
    do_output <- function(estim, pops){
        # set stdOut to sinkFile
        if (save!=F) {
            sinkFile <- nameIsFree(save)            
            sink(sinkFile, append=T, split=T)
        }
        print(paste('penalty=',pen,sep=' '))        
        print(paste('Ncycles=',Ncycles,sep=' '))    
        # print target and estimation by col
        dif <- estim - myTarget
        matrix_out <- rbind(myTarget, estim, dif)
        rownames(matrix_out)[2:3] <- c('fitted','dif')
        print(matrix_out)    
        # distance
        dist1_2 <- sqrt(sum(dif^2))
        dist1_2 <- dist1_2/PCT
        print(paste('distance%=',round(100*dist1_2,4),sep=''))
        write('',stdout())
        # table percentages by pop
        tgname <- row.names(myTarget)[1]
        write(paste('\t',tgname),stdout())
        write('',stdout())
        tb <- table(pops)
        tb <- tb[order(tb, decreasing=T)]
        tb <- as.matrix(100*tb/Nbatch)
        write.table(tb,sep=',',quote=F,col.names=F,dec='.')
        # reset sinkFile to stdOut   
        if (save!=F) {sink()}
    }   # end do_output

    # MAIN code of getMonte
    # set environment for embedded functions
    # proces input
    tempData <- read.csv(datafile, head=T, row.names=1, stringsAsFactors=T, na.strings=c('',' ','NA'))
    myData <- tempData[rownames(tempData)!=omit,]
    myTarget <- read.csv(targetfile, head=T, row.names=1)
    check_formats(myData, myTarget)
    check_omit(myData, omit)    # single item distances
    PCT <- ifelse(max(myData[1, ]>2), 100, 1)
    print('1. CLOSEST SINGLE ITEM DISTANCE%')
    print(nearestItems(myData, myTarget)*100/PCT)
    cat('\n')

    # full table nMonte
    print('2. FULL TABLE nMONTE')
    results <- do_algorithm(myData, myTarget)
    fitted <- results$estimated
    populations <- results$pops 
    do_output(fitted, populations)
    cat('\n')
    
    #print('CORRELATION OF ADMIXTURE POPULATIONS')
    #tb <- table(populations)
    #selFinal <- names(tb[tb>0])
    #adFinal <- myData[selFinal,,drop=F]
    ## catch error
    #if (nrow(adFinal)==1) {print('Only 1 population, no correlations.')}
    #else {
    #   corPops <- cor(t(adFinal))
    #    round(corPops, digits=2)
    #}

} # end getMonte function

#===================================utilities===================================
#-------------------------------------------------------------------------------
# function subset_data()
# utility for selecting rows from datasheet
# Use: subset_data('DavidMadeThis.csv', 'IselectedThis.csv' ,'Abkhasian', 'Adygei', 'Afanasievo', 'Altai_IA')
# In: name of primary dataFile, name of output file, list of selected pops from primary datafile
# Out: secondary datasheet with selected subset
# USE WITH ONE SELECTED POPULATION TO CREATE TARGET FILE
# Error message 1: non-existence or misspelled name of selected pop
# Error message 2: no pops selected
# Error message 3: output file exists, choose new name     
#-------------------------------------------------------------------------------
subset_data <- function(dataFile, saveFile, ...) {
    input <- read.csv(dataFile, head=T, row.names=1, stringsAsFactor=F)
    selection <- list(...)
    selError <- selection[!selection %in% rownames(input)]
    # test selection
    if (length(selError)>0) {
        cat(paste(selError,' is not a valid rowname\n',sep='')) }
    # output
    else {output <- input[rownames(input) %in% selection,]
          print(output)                                       # print to screen
          write.csv(output, nameIsFree(saveFile), quote=F)    # save to file 
         }
}

#-------------------------------------------------------------------------------
# function aggr_pops()
# In the files of Davidski rowlabel has the form 'pop:ID'
# This function drops the part after the colon
# and collects the mean of the pop before the colon.
# Use for mean:   aggr_pops(fileName)
# Use for median: aggr_pops(fileName, myFunc=median)
#-------------------------------------------------------------------------------
aggr_pops <- function(fileName, myFunc=mean) {
    myData <- read.csv(fileName, head=T, row.names=1, stringsAsFactors=FALSE)
    splitted <- headStrings(rownames(myData), mySep=':') 
    aggrData <- aggregate(myData, by=list(splitted), myFunc)
    temp <- as.matrix(aggrData[,-1]); rownames(temp) <- aggrData[,1]
    return(round(temp, 7))
}

#-------------------------------------------------------------------------------
# function tab2comma()
# Convert tab-separated csv to comma-separated csv
# Use: tab2comma(tabFile,commaFile)
#-------------------------------------------------------------------------------
tab2comma <- function(tabFile,commaFile) {
    data <- read.csv(tabFile, head=T, sep='\t', row.names=1, stringsAsFactor=F)
    nameIsFree(commaFile)
    write.csv(data, commaFile, row.names=T)
    }

#-------------------------------------------------------------------------------
# function nearestItems()
# Find n best matches.
# Use: inData <- read file; inTarget <- read target
#       nearestItems(inData, inTarget, maxFits=8)
# This is not the nearest neighbor algorithm;
# when the number of items is smaller than maxFits,
# functions returns all the items.
#-------------------------------------------------------------------------------
nearestItems <- function(inData, inTarget, maxFits=8) {
    totArr <- rbind(inTarget, inData)
    distMat <- as.matrix(dist(totArr, method='euclidean'))
    dist1 <- distMat[,1]
    sortDist <- dist1[order(dist1)]
    nFits <- min(nrow(inData), maxFits)
    return(sortDist[2:(nFits+1)])    
    }

#==================================internal stuff===============================
# split head from vector of strings, out vector of heads
headStrings <- function(strVec, mySep=':') {
        unlist(lapply(strsplit(strVec, mySep), function(x) x[1]))
        }

nameIsFree <- function(newFile) {
    while (file.exists(newFile)) {
        newFile <- readline('select new filename for saving (without quotes): ')
        }
    return(newFile)
    }
    
check_formats <- function(sheet, target) {
    if (any(is.na(sheet)))  {err_row <- as.integer(which(rowSums(is.na(sheet))>0))
                            print(sheet[err_row, ])
                            stop(paste('Missing value in row ',err_row))}
    if (!identical(colnames(sheet), colnames(target)))
        {print(colnames(sheet)); print(colnames(target))
         stop('Colnames input not identical')}
    }

check_omit <- function(sheet, dropInfo) {
    if (dropInfo != '' & !dropInfo %in% rownames(sheet)) {
        print('!!!! WARNING: Request to omit unknown popName. !!!!')
        }
    }